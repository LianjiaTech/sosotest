// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
// ---- ---- ---- ---- Panel

// 创建一个Panel
chrome.devtools.panels.create(

  // title
  'sosotest-network',

  // iconPath
  null,

  // pagePath
  'panel.html'
);

// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
// ---- ---- ---- ---- 任务调度

// 用于串行化处理promise
// 尤其是前一个promise还没resolved，后一个promise就已经出现的时候
const PromiseExecutor = class {
  constructor() {
    // lazy promise队列
    this._queue = [];

    // 一个变量锁，用来控制当前是否要执行队列中的lazy promise
    this._isBusy = false;
  }

  each(callback) {
    this._callback = callback;
  }

  // 通过isBusy实现加锁
  // 如果当前有任务正在执行，就返回，否则就按队列中任务的顺序来执行
  add(lazyPromise) {
    this._queue.push(lazyPromise);

    if (this._isBusy) {
      return;
    }

    this._isBusy = true;

    // execute是一个async函数，执行后立即返回，返回一个promise
    // 因此，add可以在execute内的promise resolved之前再次执行
    this.execute();
  };

  async execute() {

    // 按队列中的任务顺序来依次执行
    while (this._queue.length !== 0) {
      const head = this._queue.shift();
      const value = await head();
      this._callback && this._callback(value);
    }

    // 执行完之后，解锁
    this._isBusy = false;
  };
};

const executor = new PromiseExecutor;

// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
// ---- ---- ---- ---- http劫持

// note: 由于PromiseExecutor无法处理异常，所以异步函数需要通过返回值的状态来表示异常
const handleHttp = async args => {
  try {
    const [{
      // 请求的类型，查询参数，以及url
      request: { method, queryString, url, headers, cookies,postData},

      // 该方法可用于获取响应体
      getContent,
    }] = args;

    // 将callback转为await promise
    // warn: content在getContent回调函数中，而不是getContent的返回值
    const content = await new Promise((res, rej) => {
      return getContent(res)});

    return {
      isSuccess: true,
      data: {
        method,
        queryString,
        url,
          headers,
          cookies,
          postData,
        response: content,
      }
    };
  } catch (err) {
    return {
      isSuccess: false,
      message: err.stack || err.toString(),
    };
  }
};

// 注册一个channel用于和当前tab页的Panel进行通信
chrome.runtime.onConnect.addListener(channel => {

  // 如果channel不是来源于当前tab页，就不使用它
  if (channel.name !== chrome.devtools.inspectedWindow.tabId.toString()) {
    return;
  }

  // 作用域中留下了当前tab页的Panel所建立的channel
  chrome.devtools.network.onRequestFinished.addListener((...args) => executor.add(() => handleHttp(args)));

  // 注册回调，用来获取每个请求的所有结果
  executor.each(result => channel.postMessage(result));
});

// ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
