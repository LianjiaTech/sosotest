/*global Ext, document, jsonviewer */

/*
 * TODO:
 * keresés eltüntetéséhez gomb
 * keresésnél írjuk ki, hogy hány találat van (akár dinamikusan, hogy pörögjön felfelé)
 * about JSON Viewer ablak
 * "Format..." finomítása
 * Editable Grid
 * Griden dupla katt egy object-en, akkor válassza ki azt.
 * be lehessen állítani, hogy a kis és nagybetű számít-e?
 * tree.contextmenu (kinyít, becsuk, ?)
 * 
 */

Ext.override(Ext.tree.TreeNode, {
	removeAllChildren: function () {
		while (this.hasChildNodes()) {
			this.removeChild(this.firstChild);
		}
		return this;
	},
	setIcon: function (icon) {
		this.getUI().setIcon(icon);
	},
	setIconCls: function (icon) {
		this.getUI().setIconCls(icon);
	}
});

Ext.override(Ext.tree.TreeNodeUI, {
	setIconCls: function (iconCls) {
		if (this.iconNode) {
			Ext.fly(this.iconNode).replaceClass(this.node.attributes.iconCls, iconCls);
		}
		this.node.attributes.iconCls = iconCls;
	},
	setIcon: function (icon) {
		if (this.iconNode) {
			this.iconNode.src = icon || this.emptyIcon;
			Ext.fly(this.iconNode)[icon ? 'addClass' : 'removeClass']('x-tree-node-inline-icon');
		}
		this.node.attributes.icon = icon;
	}
});

Ext.override(Ext.Panel, {
	hideBbar: function () {
		if (!this.bbar) {
			return;
		}
		this.bbar.setVisibilityMode(Ext.Element.DISPLAY);
		this.bbar.hide();
		this.getBottomToolbar().hide();
		this.syncSize();
		if (this.ownerCt) {
			this.ownerCt.doLayout();
		}
	},
	showBbar: function () {
		if (!this.bbar) {
			return;
		}
		this.bbar.setVisibilityMode(Ext.Element.DISPLAY);
		this.bbar.show();
		this.getBottomToolbar().show();
		this.syncSize();
		if (this.ownerCt) {
			this.ownerCt.doLayout();
		}
	}
});

Ext.ux.iconCls = function () {
	var styleSheetId = 'styleSheetIconCls';
	var cssClasses = {};
	Ext.util.CSS.createStyleSheet('/* Ext.ux.iconCls */', styleSheetId);
	return {
		get: function (icon) {
			if (!icon) {
				return null;
			}
			if (typeof cssClasses[icon] === 'undefined') {
				cssClasses[icon] = 'icon_' + Ext.id();
				var styleBody = '\n.' + cssClasses[icon] + ' { background-image: url(' + icon + ') !important; }';
				if (Ext.isIE) {
					document.styleSheets[styleSheetId].cssText += styleBody;
				} else {
					Ext.get(styleSheetId).dom.sheet.insertRule(styleBody, 0);
				}
			}
			return cssClasses[icon];
		}
	};
}();

String.space = function (len) {
	var t = [], i;
	for (i = 0; i < len; i++) {
		t.push(' ');
	}
	return t.join('');
};

function aboutWindow() {
	var tabs = [];
	Ext.getBody().select('div.tab').each(function(div) {
		tabs.push({
			title: div.select('h2').first().dom.innerHTML,
			html: div.select('div').first().dom.innerHTML.replace('{gabor}', '如果觉得好用,请按Ctrl+D收藏！谢谢！')
		});
	});
	var win = new Ext.Window({
		title: document.title,
		width: 640,
		height: 400,
		modal: true,
		layout: 'fit',
		items: new Ext.TabPanel({
			defaults: {
				autoScroll: true,
				bodyStyle: 'padding: 5px;'
			},
			activeTab: 0,
			items: tabs
		})
	});
	win.show();
}

function getSelectedItems(node){
	 //var childnodes = node.childNodes||node.attributes.children;
	 var childnodes = node.attributes.children;
	 for(var i=0;i<childnodes.length;i++){  //从节点中取出子节点依次遍历
		 var rootnode = childnodes[i];
		 alert(rootnode.text);
		 if(rootnode.attributes.children.length>0){  //判断子节点下是否存在子节点，个人觉得判断是否leaf不太合理，因为有时候不是leaf的节点也可能没有子节点
			 findchildnode(rootnode);    //如果存在子节点  递归
		 }   
	 }
}

Ext.onReady(function () {

	Ext.BLANK_IMAGE_URL = 'json_resource/img/s.gif';	
	Ext.QuickTips.init();

	var ctrlF = new Ext.KeyMap(document, [{
		key: Ext.EventObject.F,
		ctrl: true,
		stopEvent: true,
		fn: function () {
			jsonviewer.ctrlF();
		}
	}, {
		key: Ext.EventObject.H,
		ctrl: true,
		stopEvent: true,
		fn: function () {
			jsonviewer.hideToolbar();
		}
	}]);
	ctrlF.disable();
	
	var grid = {
		xtype: 'propertygrid',
		id: 'grid',
		region: 'east',
		width: 300,
		split: true,
	    listeners: {
	    	beforeedit: function () {
	    		return false;
	    	}
	    },
	    selModel: new Ext.grid.RowSelectionModel(),
	    onRender: Ext.grid.PropertyGrid.superclass.onRender
	};
    var tree = {
    	id: 'tree',
    	xtype: 'treepanel',
    	region: 'center',
		loader: new Ext.tree.TreeLoader(),
		lines: true, 
        root: new Ext.tree.TreeNode({text: 'JSON'}),
        autoScroll: true,
        trackMouseOver: false,
        listeners: {
        	render: function (tree) {
        		tree.getSelectionModel().on('selectionchange', function (tree, node) {
        			jsonviewer.gridbuild(node);
        		});
				
				tree.on('contextmenu',function(node,e){
				//var selectNode = tree.getSelectionModel().getLastSelected();
				//	alert(selectNode.data);
				
				var menu=new Ext.menu.Menu({
			      minWidth:120,	
			   items:[               
			           {text:'复制Key',
						iconCls:'newdep_images',  //样式
						id:"copyItem",
						handler:function(){

						window.prompt("请复制",node.text.split(":")[0]);
						}
						},
						{text:'复制Value',
						iconCls:'newdep_images',  //样式
						handler:function(){
						window.prompt("请复制",node.text.split(":")[1]);
						}
						} ,
						{text:'复制Key+Value',
						iconCls:'newdep_images',  //样式
						handler:function(){
						window.prompt("请复制",node.text);
						}
						},{text:'展开所有子节点',
						iconCls:'newdep_images',  //样式
						id:"exp_Item",
						handler:function(){
							node.expand(true);          
							/*node.eachChild(function(child) {
							child.expand();   
							});*/ 
						}},
						{text:'展开所有节点',
						iconCls:'newdep_images',  //样式
						id:"exp_All",
						handler:function(){
							tree.getRootNode().expand(true);
						}}, 
						{text:'收起所有子节点',
						iconCls:'newdep_images',  //样式
						id:"hide_Item",
						handler:function(){
							node.collapse(true);          
							/*node.eachChild(function(child) {
							child.expand();   
							});*/ 
						}},
						{text:'收起所有节点',
						iconCls:'newdep_images',  //样式
						id:"hide_All",
						handler:function(){
							tree.getRootNode().collapse(true);
						}}
					]
				})
				menu.showAt(e.getPoint());
					var x= '';
			  }); 
        	}
        },
        bbar: [
        	'Search:',
        	new Ext.form.TextField({
				xtype: 'textfield',
				id: 'searchTextField'
	        }),
	        new Ext.Button({
	        	text: 'GO!',
	        	handler:  function () {
	        		jsonviewer.searchStart();
	        	}
	        }),
	        new Ext.form.Label({
	        	id: 'searchResultLabel',
	        	style: 'padding-left:10px;font-weight:bold'
	        }), {
	        	iconCls: Ext.ux.iconCls.get('json_resource/img/arrow_down.png'),
	        	text: 'Next',
	        	handler: function () {
	        		jsonviewer.searchNext();
	        	}
	        }, {
	        	iconCls: Ext.ux.iconCls.get('json_resource/img/arrow_up.png'),
	        	text: 'Previous',
	        	handler: function () {
	        		jsonviewer.searchPrevious();
	        	}
	        }
		]
    };
	var edit = {
		id: 'edit',
		xtype: 'textarea',
		style: 'font-family:monospace',
		emptyText: '将JSON数据粘贴到这里!',
		selectOnFocus: true
	};
	var viewerPanel = {
		id: 'viewerPanel',
		layout: 'border',
		title: '视图',
		items: [tree, grid]
	};
	var textPanel = {
		id: 'textPanel',
		layout: 'fit',
		title: 'JSON数据',
		tbar: [
			{text: '格式化', handler: function () {
				jsonviewer.format();
			}},
			'-',
			{text: '删除空格', handler: function () {
				jsonviewer.removeWhiteSpace();
			}},
			'-',
			{text: '删除空格并转义', handler: function () {
				jsonviewer.removeWhiteSpace2();
			}},
			'-',
			{text: '去除转义', handler: function () {
				jsonviewer.removeZhuanyi();
			}},
			'->',
			{text: '回到首页', handler: function(){
        window.location.href="http://t127.cassie.wang/";
			}}
		],
		items: edit
	};
	var vp = new Ext.Viewport({
		layout: 'fit',
		items: {
			xtype: 'tabpanel',
			items: [viewerPanel, textPanel],
			activeTab: 'textPanel',
			listeners: {
				beforetabchange: function (tabpanel, tab) {
					if (tab.id === 'viewerPanel') {
						return jsonviewer.check();
					}
				},
				tabchange: function (tabpanel, tab) {
					if (tab.id === 'viewerPanel') {
						ctrlF.enable();
					} else {
						ctrlF.disable();
					}
				}
			}
		}
	});

	var jsonviewer = function () {
		var edit = Ext.getCmp('edit');
		var tree = Ext.getCmp('tree');
		var root = tree.getRootNode();
		var grid = Ext.getCmp('grid');
		var searchTextField = Ext.getCmp('searchTextField');
		var searchResultLabel = Ext.getCmp('searchResultLabel');
		var json = {};
		var lastText = null;
		var task = null;
		var searchList = null;
		var searchIndex = null;
		return {
			check: function () {
				// üres sorok törlése:
				var text = edit.getValue().split("\n").join(" ");
				try {
					json = Ext.util.JSON.decode(text);
				} catch (e) {
					Ext.MessageBox.show({
						title: 'JSON 错误',
						msg: 'JSON 格式错误',
						icon: Ext.MessageBox.ERROR,
						buttons: Ext.MessageBox.OK,
						closable: false
					});
					return false;
				}
				if (lastText === text) {
					return;
				}
				lastText = text;
				this.treebuild();
			},
			treebuild: function () {
				root.removeAllChildren();
				root.appendChild(this.json2leaf(json));
				root.setIcon(Ext.isArray(json) ? 'json_resource/img/array.gif' : 'json_resource/img/object.gif');
				this.gridbuild(root);
			},
			gridbuild: function (node) {
				if (node.isLeaf()) {
					node = node.parentNode;
				}
				// elofordulhat, hogy nincsen még kifejtve:
				if (!node.childNodes.length) {
					node.expand(false, false);
					node.collapse(false, false);
				}
				var source = {};
				for (var i = 0; i < node.childNodes.length; i++) { 
					var t = node.childNodes[i].text.split(':');
					if (t.length > 1) {
						source[t[0]] = t[1];
					} else {
						source[t[0]] = '...';
					}
				}
				grid.setSource(source);
			},
			json2leaf: function (json) {
				var ret = [];
				for (var i in json) {
					if (json.hasOwnProperty(i)) {
						if (json[i] === null) {
							ret.push({text: i + ' : null', leaf: true, icon: 'json_resource/img/red.gif'});
						} else if (typeof json[i] === 'string') {
							ret.push({text: i + ' : "' + json[i] + '"', leaf: true, icon: 'json_resource/img/blue.gif'});
						} else if (typeof json[i] === 'number') {
							ret.push({text: i + ' : ' + json[i], leaf: true, icon: 'json_resource/img/green.gif'});
						} else if (typeof json[i] === 'boolean') {
							ret.push({text: i + ' : ' + (json[i] ? 'true' : 'false'), leaf: true, icon: 'json_resource/img/yellow.gif'});
						} else if (typeof json[i] === 'object') {
							ret.push({text: i, children: this.json2leaf(json[i]), icon: Ext.isArray(json[i]) ? 'json_resource/img/array.gif' : 'json_resource/img/object.gif'});
						} else if (typeof json[i] === 'function') {
							ret.push({text: i + ' : function', leaf: true, icon: 'json_resource/img/red.gif'});
						}
					}
				}
				return ret;
			},
			copyText: function () {
				if (!edit.getValue()) {
					return;
				}
				Ext.ux.Clipboard.set(edit.getValue());
			},
			pasteText: function () {
				edit.setValue(Ext.ux.Clipboard.get());
			},
			searchStart: function () {
				if (!task) {
					task = new Ext.util.DelayedTask(this.searchFn, this);
				}
				task.delay(150);
			},
			searchFn: function () {
				searchList = [];
				if (!searchTextField.getValue()) {
					return;
				}
				this.searchInNode(root, searchTextField.getValue());
				if (searchList.length) {
					searchResultLabel.setText('');
					searchIndex = 0;
					this.selectNode(searchList[searchIndex]);
					searchTextField.focus();
				} else {
					searchResultLabel.setText('Phrase not found!');
				}
			},
			searchInNode: function (node, text) {
				if (node.text.toUpperCase().indexOf(text.toUpperCase()) !== -1) {
					searchList.push(node);
					//return true;
				}
				var isExpanded = node.isExpanded();
				node.expand(false, false);
				for (var i = 0; i < node.childNodes.length; i++) {
					if (this.searchInNode(node.childNodes[i], text)) {
						//return true;
					}
				}
				if (!isExpanded) {
					node.collapse(false, false);
				}
				//return false;
			},
			selectNode: function (node) {
				node.select();
				tree.fireEvent('click', node);
				while (node !== root) {
					node = node.parentNode;
					node.expand(false, false);
				}				
			},
			searchNext: function () {
				if (!searchList || !searchList.length) {
					return;
				}
				searchIndex = (searchIndex + 1) % searchList.length;
				this.selectNode(searchList[searchIndex]);
			},
			searchPrevious: function () {
				if (!searchList || !searchList.length) {
					return;
				}
				searchIndex = (searchIndex - 1 + searchList.length) % searchList.length;
				this.selectNode(searchList[searchIndex]);
			},
			ctrlF: function () {
				if (!tree.getBottomToolbar().isVisible()) {
					tree.showBbar();
				}
				searchTextField.focus(true);
			},
			hideToolbar: function () {
				tree.hideBbar();
			},
			format: function () {
				var text = edit.getValue().split("\n").join(" ");
				var t = [];
				var tab = 0;
				var inString = false;
				for (var i = 0, len = text.length; i < len; i++) {
					var c = text.charAt(i);
					if (inString && c === inString) {
						// TODO: \\"
						if (text.charAt(i - 1) !== '\\') {
							inString = false;
						}
					} else if (!inString && (c === '"' || c === "'")) {
						inString = c;
					} else if (!inString && (c === ' ' || c === "\t")) {
						c = '';
					} else if (!inString && c === ':') {
						c += ' ';
					} else if (!inString && c === ',') {
						c += "\n" + String.space(tab * 2);
					} else if (!inString && (c === '[' || c === '{')) {
						tab++;
						c += "\n" + String.space(tab * 2);
					} else if (!inString && (c === ']' || c === '}')) {
						tab--;
						c = "\n" + String.space(tab * 2) + c;
					}
					t.push(c);
				}
				edit.setValue(t.join(''));
			},
			removeWhiteSpace:function(){
				edit.setValue(jsonviewer.getRemoveWhiteSpace());
			}
			,
			getRemoveWhiteSpace: function () {
				var text = edit.getValue().split("\n").join(" ");
				var t = [];
				var inString = false;
				for (var i = 0, len = text.length; i < len; i++) {
					var c = text.charAt(i);
					if (inString && c === inString) {
						// TODO: \\"
						if (text.charAt(i - 1) !== '\\') {
							inString = false;
						}
					} else if (!inString && (c === '"' || c === "'")) {
						inString = c;
					} else if (!inString && (c === ' ' || c === "\t")) {
						c = '';
					}
					t.push(c);
				}
				return t.join('');
			},
			removeWhiteSpace2: function (){
				var a = jsonviewer.getRemoveWhiteSpace().replace(/\"/g,"\\\"");
				edit.setValue(a);
			},
			removeZhuanyi: function (){
				var a = edit.getValue().replace(/\\\\/g,"\\").replace(/\\\"/g,'\"');
				edit.setValue(a);
			}
			
		};
	}();
});