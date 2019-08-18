// CodeMirror, copyright (c) by Marijn Haverbeke and others
// Distributed under an MIT license: http://codemirror.net/LICENSE

//变量 定义
var allKeyList = new Array();
//小括号计数
var allKeySmallIndex = 0;
//中括号计数
var allBracketIndex = 0;
(function(mod) {
  if (typeof exports == "object" && typeof module == "object") // CommonJS
    mod(require("../../lib/codemirror"));
  else if (typeof define == "function" && define.amd) // AMD
    define(["../../lib/codemirror"], mod);
  else // Plain browser env
    mod(CodeMirror);
})(function(CodeMirror) {
  "use strict";

  function wordRegexp(words) {
    return new RegExp("^((" + words.join(")|(") + "))\\b");
  }

  var wordOperators = wordRegexp(["and", "or", "not", "is"]);
  var commonKeywords = ["as", "assert", "break", "class", "continue",
                        "def", "del", "elif", "else", "except", "finally",
                        "for", "from", "global", "if", "import",
                        "lambda", "pass", "raise", "return",
                        "try", "while", "with", "yield", "in"];
  var commonBuiltins = ["abs", "all", "any", "bin", "bool", "bytearray", "callable", "chr",
                        "classmethod", "compile", "complex", "delattr", "dict", "dir", "divmod",
                        "enumerate", "eval", "filter", "float", "format", "frozenset",
                        "getattr", "globals", "hasattr", "hash", "help", "hex", "id",
                        "input", "int", "isinstance", "issubclass", "iter", "len",
                        "list", "locals", "map", "max", "memoryview", "min", "next",
                        "object", "oct", "open", "ord", "pow", "property", "range",
                        "repr", "reversed", "round", "set", "setattr", "slice",
                        "sorted", "staticmethod", "str", "sum", "super", "tuple",
                        "type", "vars", "zip", "__import__", "NotImplemented",
                        "Ellipsis", "__debug__"];
  CodeMirror.registerHelper("hintWords", "python", commonKeywords.concat(commonBuiltins));

  function top(state) {
    allKeyList = [];
    allKeySmallIndex = 0;
    allBracketIndex = 0;
    return state.scopes[state.scopes.length - 1];
  }

  CodeMirror.defineMode("python", function(conf, parserConf) {

    var ERRORCLASS = "error";
    var singleDelimiters = parserConf.singleDelimiters || /^[\(\)\[\]\{\}@,:`=;\.]/;
    var doubleOperators = parserConf.doubleOperators || /^([!<>]==|<>|<<|>>|\/\/|\*\*)/;
    var doubleDelimiters = parserConf.doubleDelimiters || /^(\+=|\-=|\*=|%=|\/=|&=|\|=|\^=)/;
    var tripleDelimiters = parserConf.tripleDelimiters || /^(\/\/=|>>=|<<=|\*\*=)/;

    var hangingIndent = parserConf.hangingIndent || conf.indentUnit;

    var myKeywords = commonKeywords, myBuiltins = commonBuiltins;
    if (parserConf.extra_keywords != undefined)
      myKeywords = myKeywords.concat(parserConf.extra_keywords);

    if (parserConf.extra_builtins != undefined)
      myBuiltins = myBuiltins.concat(parserConf.extra_builtins);

    var py3 = true;
    if (py3) {
      // since http://legacy.python.org/dev/peps/pep-0465/ @ is also an operator
      var singleOperators = parserConf.singleOperators || /^[\+\-\*\/%&|\^~<>!@]/;
      var identifiers = parserConf.identifiers|| /^[_A-Za-z\u00A1-\uFFFF][_A-Za-z0-9\u00A1-\uFFFF]*/;
      myKeywords = myKeywords.concat(["nonlocal", "False", "True", "None", "async", "await","context"]);
      myBuiltins = myBuiltins.concat(["ascii", "bytes", "exec", "print"]);
      //添加sosotest的pythonmode的内置函数
      myBuiltins = myBuiltins.concat(["assert_struct","asserts","call","const","db_delete","db_insert","db_select","db_update",
                                    "execute_current","execute_dubbo_interface","execute_interface","execute_testcase",
                                    "gvar","imports","log","redis_del","redis_get","redis_set",
                                    "set_result","text","var"]);
      var stringPrefixes = new RegExp("^(([rbuf]|(br))?('{3}|\"{3}|['\"]))", "i");
    } else {
      var singleOperators = parserConf.singleOperators || /^[\+\-\*\/%&|\^~<>!]/;
      var identifiers = parserConf.identifiers|| /^[_A-Za-z][_A-Za-z0-9]*/;
      myKeywords = myKeywords.concat(["exec", "print"]);
      myBuiltins = myBuiltins.concat(["apply", "basestring", "buffer", "cmp", "coerce", "execfile",
                                      "file", "intern", "long", "raw_input", "reduce", "reload",
                                      "unichr", "unicode", "xrange", "False", "True", "None"]);
      var stringPrefixes = new RegExp("^(([rubf]|(ur)|(br))?('{3}|\"{3}|['\"]))", "i");
    }
    var keywords = wordRegexp(myKeywords);
    var builtins = wordRegexp(myBuiltins);

      // my reg function
  function wordRegexpMyKeywords(words) {
    return new RegExp("^((" + words.join(")|(") + "))\\(");
  }
  function wordRegexpMyVars(words) {
    return new RegExp("^((\\" + words.join(")|(\\") + "))\\[");
  }

    // tokenizers
    function tokenBase(stream, state) {

      if (stream.sol()) state.indent = stream.indentation()
      // Handle scope changes
      if (stream.sol() && top(state).type == "py") {
        var scopeOffset = top(state).offset;
        if (stream.eatSpace()) {
          var lineOffset = stream.indentation();
          if (lineOffset > scopeOffset)
            pushPyScope(state);
          else if (lineOffset < scopeOffset && dedent(stream, state) && stream.peek() != "#")
            state.errorToken = true;
          return null;
        } else {
          var style = tokenBaseInner(stream, state);
          if (scopeOffset > 0 && dedent(stream, state))
            style += " " + ERRORCLASS;
          return style;
        }
      }
      return tokenBaseInner(stream, state);
    }

    function tokenBaseInner(stream, state) {
      if (stream.eatSpace()) return null;

      var ch = stream.peek();

      // Handle Comments
      if (ch == "#") {
        stream.skipToEnd();
        return "comment";
      }
      // soso关键字 new RegExp("^((" + words.join(")|(") + "))\\(")  || stream.match(/^.*\)/)
      var sosoKeywords = ['DB_SELECT', 'DB_UPDATE', 'DB_DELETE', 'DB_INSERT', 'REDIS_SET', 'REDIS_GET', 'REDIS_DEL', 'EXECUTE_INTERFACE', 'EXECUTE_TESTCASE', 'EXECUTE_DUBBO_INTERFACE', 'EVAL', 'EXEC_PYTHON', 'ASSERT', 'ASSERT_STRUCT', 'JSON_PATH_GET','JSON_PATH_GET_FIRST', 'JSON_GET', 'JSON_PATH_EXIST', 'JSON_LIST_LEN', 'GET_JSON_KEYS_LIST', 'GET_JSON_KEY_BY_INDEX', 'GET_JSON_FROM_LIST_BY_KEYVALUE', 'GET_LIST_KEY_VALUE_TO_STRING_WITH_SPLIT_TAG', 'SUB_STR', 'RE_FINDALL', 'BS_FIND', 'RANDOM_INT', 'RANDOM_EN', 'RANDOM_CN', 'RANDOM_VALUE_IN_LIST', 'URL_ENCODE', 'MD5', 'STR_TO_LOWER', 'STR_TO_UPPER', 'DATETIME_FORMAT', 'SPECIAL_TIMESTAMP', 'TIMESTAMP', 'TIMESTAMP_FORMAT', 'DAYS_OF_MONTH', 'TIME_SLEEP', 'SPECIAL_TIMESTAMP_MS', 'TIMESTAMP_MS', 'TIMESTAMP_FORMAT_MS'];
      var self_data_keyword = ['GET_TOKEN','LOGIN_LJ','LOGIN', 'LOGIN_CAS','LOGIN_SHIRO_CAS','LOGIN_COMMERCE','API_LOGIN'];
      var allKeywordsList = sosoKeywords.concat(self_data_keyword);
      var sosoKeywordsMatch = wordRegexpMyKeywords(allKeywordsList );
        if ( stream.match(sosoKeywordsMatch) )
        return "keyword";
      // soso变量全局等  stream.match(/^(self|cls)\b/)    || stream.match(/^.*\]/)
      var myVarsList = ["$GVAR","$VAR","$CONST","$TEXT","$IMPORT","$RUNFUNC"];
      var myVarsReg = wordRegexpMyVars(myVarsList);
      if (stream.match(myVarsReg)  )
        return "variable-2";

      // Handle Number Literals
      if (stream.match(/^[0-9\.]/, false)) {
        var floatLiteral = false;
        // Floats
        if (stream.match(/^[\d_]*\.\d+(e[\+\-]?\d+)?/i)) { floatLiteral = true; }
        if (stream.match(/^[\d_]+\.\d*/)) { floatLiteral = true; }
        if (stream.match(/^\.\d+/)) { floatLiteral = true; }
        if (floatLiteral) {
          // Float literals may be "imaginary"
          stream.eat(/J/i);
          return "number";
        }
        // Integers
        var intLiteral = false;
        // Hex
        if (stream.match(/^0x[0-9a-f_]+/i)) intLiteral = true;
        // Binary
        if (stream.match(/^0b[01_]+/i)) intLiteral = true;
        // Octal
        if (stream.match(/^0o[0-7_]+/i)) intLiteral = true;
        // Decimal
        if (stream.match(/^[1-9][\d_]*(e[\+\-]?[\d_]+)?/)) {
          // Decimal literals may be "imaginary"
          stream.eat(/J/i);
          // TODO - Can you have imaginary longs?
          intLiteral = true;
        }
        // Zero by itself with no other piece of number.
        if (stream.match(/^0(?![\dx])/i)) intLiteral = true;
        if (intLiteral) {
          // Integer literals may be "long"
          stream.eat(/L/i);
          return "number";
        }
      }

      // Handle Strings
      if (stream.match(stringPrefixes)) {
        state.tokenize = tokenStringFactory(stream.current());
        return state.tokenize(stream, state);
      }

      // Handle operators and Delimiters
      if (stream.match(tripleDelimiters) || stream.match(doubleDelimiters))
        return "punctuation";

      if (stream.match(doubleOperators) || stream.match(singleOperators))
        return "operator";

      if (stream.match(singleDelimiters))
        return "punctuation";

      if (state.lastToken == "." && stream.match(identifiers))
        return "property";

      if (stream.match(keywords) || stream.match(wordOperators))
        return "keyword";

      if (stream.match(builtins))
        return "builtin";

      if (stream.match(/^(self|cls)\b/))
        return "variable-2";

      if (stream.match(identifiers)) {
        if (state.lastToken == "def" || state.lastToken == "class")
          return "def";
        return "variable";
      }

      // Handle non-detected items
      stream.next();
      return ERRORCLASS;
    }

    function tokenStringFactory(delimiter) {

      while ("rubf".indexOf(delimiter.charAt(0).toLowerCase()) >= 0)
        delimiter = delimiter.substr(1);

      var singleline = delimiter.length == 1;
      var OUTCLASS = "string";

      function tokenString(stream, state) {
        while (!stream.eol()) {
          stream.eatWhile(/[^'"\\]/);
          if (stream.eat("\\")) {
            stream.next();
            if (singleline && stream.eol())
              return OUTCLASS;
          } else if (stream.match(delimiter)) {
            state.tokenize = tokenBase;
            return OUTCLASS;
          } else {
            stream.eat(/['"]/);
          }
        }
        if (singleline) {
          if (parserConf.singleLineStringErrors)
            return ERRORCLASS;
          else
            state.tokenize = tokenBase;
        }
        return OUTCLASS;
      }
      tokenString.isString = true;
      return tokenString;
    }

    function pushPyScope(state) {
      while (top(state).type != "py") state.scopes.pop()
      state.scopes.push({offset: top(state).offset + conf.indentUnit,
                         type: "py",
                         align: null})
    }

    function pushBracketScope(stream, state, type) {
      var align = stream.match(/^([\s\[\{\(]|#.*)*$/, false) ? null : stream.column() + 1
      state.scopes.push({offset: state.indent + hangingIndent,
                         type: type,
                         align: align})
    }

    function dedent(stream, state) {
      var indented = stream.indentation();
      while (state.scopes.length > 1 && top(state).offset > indented) {
        if (top(state).type != "py") return true;
        state.scopes.pop();
      }
      return top(state).offset != indented;
    }

    function tokenLexer(stream, state) {
      if (stream.sol()) state.beginningOfLine = true;

      var style = state.tokenize(stream, state);
      var current = stream.current();

      // Handle decorators
      if (state.beginningOfLine && current == "@")
        return stream.match(identifiers, false) ? "meta" : py3 ? "operator" : ERRORCLASS;

      if (/\S/.test(current)) state.beginningOfLine = false;

      if ((style == "variable" || style == "builtin")
          && state.lastToken == "meta")
        style = "meta";

      // Handle scope changes.
      if (current == "pass" || current == "return")
        state.dedent += 1;

      if (current == "lambda") state.lambda = true;
      if (current == ":" && !state.lambda && top(state).type == "py")
        pushPyScope(state);

      var delimiter_index = current.length == 1 ? "[({".indexOf(current) : -1;
      allKeyList.push(current.replace(/\"(.+?)\"/g,""));
      if (delimiter_index != -1)
        if (current === "("){
          return "keyword"
        }else if(current === "["){
          return "variable-2"
        }

      delimiter_index = "])}".indexOf(current);
      if (delimiter_index != -1) {
        if (current === ")"){
          allKeySmallIndex += 1;
          var smallFlag = 0;
          for(var index = 0;index < allKeyList.length;index ++){
              smallFlag += allKeyList[index].split("(").length - 1;
          }
          console.log("smallFlag   "  + smallFlag)
          console.log("allKeySmallIndex   "  + allKeySmallIndex)
          if(allKeySmallIndex <= smallFlag){
            return "keyword";
          }else {
            return ERRORCLASS;
          }
          // return "keyword"
        }else if(current === "]"){
          allBracketIndex += 1;
          var smallFlag = 0;
          for(var index = 0;index < allKeyList.length;index ++){
              smallFlag += allKeyList[index].split("[").length - 1;
          }
          if(allBracketIndex <= smallFlag){
            return "variable-2"
          }else {
            return ERRORCLASS;
          }
        }

        // if (top(state).type == current) state.indent = state.scopes.pop().offset - hangingIndent
        // else return ERRORCLASS;
      }
      if (state.dedent > 0 && stream.eol() && top(state).type == "py") {
        if (state.scopes.length > 1) state.scopes.pop();
        state.dedent -= 1;
      }

      return style;
    }

    var external = {
      startState: function(basecolumn) {
        return {
          tokenize: tokenBase,
          scopes: [{offset: basecolumn || 0, type: "py", align: null}],
          indent: basecolumn || 0,
          lastToken: null,
          lambda: false,
          dedent: 0
        };
      },

      token: function(stream, state) {
        var addErr = state.errorToken;
        if (addErr) state.errorToken = false;
        var style = tokenLexer(stream, state);
        if (style && style != "comment")
          state.lastToken = (style == "keyword" || style == "punctuation") ? stream.current() : style;
        if (style == "punctuation") style = null;

        if (stream.eol() && state.lambda)
          state.lambda = false;
        return addErr ? style + " " + ERRORCLASS : style;
      },

      indent: function(state, textAfter) {
        if (state.tokenize != tokenBase)
          return state.tokenize.isString ? CodeMirror.Pass : 0;

        var scope = top(state), closing = scope.type == textAfter.charAt(0)
        if (scope.align != null)
          return scope.align - (closing ? 1 : 0)
        else
          return scope.offset - (closing ? hangingIndent : 0)
      },

      electricInput: /^\s*[\}\]\)]$/,
      closeBrackets: {triples: "'\""},
      lineComment: "#",
      fold: "indent"
    };

    return external;
  });

  CodeMirror.defineMIME("text/x-python", "python");

  var words = function(str) { return str.split(" "); };

  CodeMirror.defineMIME("text/x-cython", {
    name: "python",
    extra_keywords: words("by cdef cimport cpdef ctypedef enum except"+
                          "extern gil include nogil property public"+
                          "readonly struct union DEF IF ELIF ELSE")
  });

});