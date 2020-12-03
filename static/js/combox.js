var Combox=function(elem,options){this.elem=$(elem);this.options=$.extend(true,{},this.options,options);this.init();}
Combox.prototype={options:{data:[],itemclick:null,selectData:[],filterText:'',filterData:[],height:'180px',id:"id",name:"name",filterField:"name",inputClick:function(){},valueChange:function(){}},init:function(){var me=this,opt=me.options,elem=me.elem;opt.filterField=opt.name;var id=elem[0].id;var combListId=opt.combListId=id+"-container";elem.addClass('combox-box');elem.attr("autocomplete","off");elem.attr("readonly","readonly");if($("#"+combListId).length>0){$("#"+combListId).remove();$(document).off("mousedown","#"+id);$(document).off("mousedown");$(document).off("mousedown",".search-check");$(document).off("input",".search-check");$(document).off("mousedown","#"+combListId+" .check-item");$(document).off("mousedown","#"+combListId+" .checkAll");}
me.loadData(opt.data);$(document).on("mousedown","#"+id,function(e){e.stopPropagation();$("#"+id+"-container").toggleClass("active");me.options.inputClick.call(this,$("#"+id+"-container"));var offsetnum=me._calcOffset($(this));$("#"+id+"-container").css({width:offsetnum.width,left:offsetnum.left,top:offsetnum.top+offsetnum.height,})
opt.filterText='';opt.filterData=me._toFilter(opt.data,opt.filterText,opt.filterField);me._renderComboxList();if($(".check-item").length==$(".check-item.checked").length&&$(".check-item").length>0){$("#"+combListId+" .checkAll").addClass("checked");}
else if($("#"+combListId+" .checkAll").hasClass("checked")){$("#"+combListId+" .checkAll").removeClass("checked");}})
$(document).on("mousedown",function(e){e.stopPropagation();$("#"+id+"-container").removeClass("active");})
$(document).on("mousedown",".search-check",function(e){e.stopPropagation();})
$(document).on("input",".search-check",function(e){opt.filterText=$(this).val();opt.filterData=me._toFilter(opt.data,opt.filterText,opt.filterField);me._renderComboxListBody();if($(".check-item").length==$(".check-item.checked").length&&$(".check-item").length>0){$("#"+combListId+" .checkAll").addClass("checked");}
else if($("#"+combListId+" .checkAll").hasClass("checked")){$("#"+combListId+" .checkAll").removeClass("checked");}})
$(document).on("mousedown","#"+combListId+" .check-item",function(e){e.stopPropagation();var selectId=this.id;$(this).toggleClass("checked");if($(this).hasClass("checked")){var item=me.getDataById(selectId);opt.selectData.push(item);}
else{opt.selectData=opt.selectData.reduce(function(res,item){if(item[opt.id]!=selectId){res.push(item);}
return res;},[]);}
if($(".check-item").length==$(".check-item.checked").length&&$(".check-item").length>0){$("#"+combListId+" .checkAll").addClass("checked");}
else if($("#"+combListId+" .checkAll").hasClass("checked")){$("#"+combListId+" .checkAll").removeClass("checked");}
me._showSelectText($("#"+id));me._assignSelectData();opt.valueChange.call(me,{data:opt.data,filterData:opt.filterData,selectData:opt.selectData});});$(document).on("mousedown","#"+combListId+" .checkAll",function(e){e.stopPropagation();$(this).toggleClass("checked");if($(this).hasClass("checked")){$("#"+combListId).find(".check-item").addClass("checked");opt.selectData=opt.selectData.concat(opt.filterData);}
else{$("#"+combListId).find(".check-item").removeClass("checked");var _selectData=[];for(var i=0;i<opt.selectData.length;i++){_selectData[opt.selectData[i][opt.id]]=opt.selectData[i];}
for(var j=0;j<opt.filterData.length;j++){if(_selectData[opt.filterData[j][opt.id]]){delete _selectData[opt.filterData[j][opt.id]];}}
opt.selectData=Object.values(_selectData);}
me._assignSelectData();me._showSelectText($("#"+id));opt.valueChange.call(opt,{data:opt.data,filterData:opt.filterData,selectData:opt.selectData});})},loadData:function(data){this.options.data=data||[];if(this.options.data instanceof Array===false){throw "数据格式错误！"}
else if(!this.options.data.length){return false;}
this._initSelected(this.options.data);this.refresh();},refresh:function(){this._render();},getDataById:function(id){var data=this.options.data;for(var i=0;i<data.length;i++){var item=data[i];if(item[this.options.id]==id){return item;}}},getSelectId:function(){var selectData=this.options.selectData;return selectData.map(item=>item[this.options.id]);},_render:function(){var data=this.options.data||[];this.options.filterData=this._toFilter(data,this.options.filterText,this.options.filterField);this._renderCombox(data);this._showSelectText(this.elem);},_showSelectText:function(elem){var me=this,opt=me.options,selectData=opt.selectData;var jointext=[]
for(var i=0;i<selectData.length;i++){if(typeof(opt.name)==="string"){jointext.push(opt.selectData[i][opt.name]);}
else{jointext.push(opt.selectData[i][opt.name[0]]);}}
if(elem[0].tagName==="INPUT"){elem.val(jointext.join(","));}
else{elem.text(jointext.join(","));}
elem.attr("title",jointext.join("，"));},_initSelected:function(data){var me=this;for(var i=0;i<data.length;i++){if(data[i].checked){me.options.selectData.push(data[i]);}}},_toFilter:function(data,filterText,filterField){if(typeof(filterField)==="string"){return data.filter(function(value){return value[filterField].indexOf(filterText)>-1})}
else{return data.filter(function(value){var isFind=false;for(var i=0;i<filterField.length;i++){var _item=filterField[i];if(value[_item].indexOf(filterText)>-1){isFind=true}}
return isFind;})}},_renderCombox:function(data){var me=this,elem=me.elem,opt=me.options,combListId=opt.combListId;var offsetnum=me._calcOffset(elem);var sb=['<div id="'+combListId+'" class="combox-warpper"  style="position:absolute;width:'+offsetnum.width+'px;left:'+offsetnum.left+'px;top:'+(offsetnum.top+offsetnum.height)+'px;height:'+opt.height+'">'];sb[sb.length]='</div>';$(document.body).append(sb.join(""));this._renderComboxList();},_calcOffset:function(elem){var width=elem.outerWidth();var height=elem.outerHeight();var left=elem.offset().left;var top=elem.offset().top;return{width:width,height:height,left:left,top:top}},_renderComboxList:function(){var me=this,opt=me.options;var filterData=opt.filterData;var sb=[];sb[sb.length]='<ul >';sb[sb.length]='</ul>';sb[sb.length]='<input placeholder="回车查询" class="search-check" autocomplete="off" value='+opt.filterText+'>';$("#"+opt.combListId+".combox-warpper").html(sb.join(""));me._renderComboxListBody();},_renderComboxListBody(){var me=this,opt=me.options;var filterData=opt.filterData;var sb=[];sb[sb.length]='<li class="checkAll"><i class="check-icon"></i>全选</li>';for(var i=0;i<filterData.length;i++){var item=filterData[i];sb[sb.length]='<li id="'+item[opt.id]+'" class="check-item';if(item.checked){sb[sb.length]=' checked ';}
if(typeof(opt.name)=="string"){sb[sb.length]='"><i class="check-icon"></i>'+item[opt.name]+'</li>';}
else{sb[sb.length]='"><i class="check-icon"></i>';for(var j=0;j<opt.name.length;j++){sb[sb.length]=item[opt.name[j]];if(j!==opt.name.length-1){sb[sb.length]="-";}}
sb[sb.length]='</li>';}}
$("#"+opt.combListId+".combox-warpper ul").html(sb.join(""));},_assignSelectData(){var me=this,opt=me.options;selectdata=opt.selectData,data=opt.data;data=data.concat(selectdata);data=data.reduce(function(res,item){item.checked=false;if(res[item[opt.id]]){res[item[opt.id]]["checked"]=true;}
else{res[item[opt.id]]=item;}
return res;},{});opt.data=Object.values(data);opt.selectData=opt.data.filter(function(val){return val.checked;});}}
$.fn.combox=function(options){var isSTR=typeof options=="string",args,ret;if(isSTR){args=$.makeArray(arguments)
args.splice(0,1);}
var name="combox",type=Combox;var jq=this.each(function(){var ui=$.data(this,name);if(!ui){ui=new type(this,options);$.data(this,name,ui);}
if(isSTR){ret=ui[options].apply(ui,args);}});return isSTR?ret:jq;};