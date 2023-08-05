!function(a){"function"==typeof define&&define.amd?define("plone_app_imagecropping_cropper",["jquery"],a):a("object"==typeof exports?require("jquery"):jQuery)}(function(a){"use strict";function b(a){return"number"==typeof a&&!isNaN(a)}function c(a){return"undefined"==typeof a}function d(a,c){var d=[];return b(c)&&d.push(c),d.slice.apply(a,d)}function e(a,b){var c=d(arguments,2);return function(){return a.apply(b,c.concat(d(arguments)))}}function f(a){var b=a.match(/^(https?:)\/\/([^\:\/\?#]+):?(\d*)/i);return b&&(b[1]!==u.protocol||b[2]!==u.hostname||b[3]!==u.port)}function g(a){var b="timestamp="+(new Date).getTime();return a+(-1===a.indexOf("?")?"?":"&")+b}function h(a){return a?' crossOrigin="'+a+'"':""}function i(a,b){var c;return a.naturalWidth&&!qa?b(a.naturalWidth,a.naturalHeight):(c=document.createElement("img"),c.onload=function(){b(this.width,this.height)},void(c.src=a.src))}function j(a){var c=[],d=a.rotate,e=a.scaleX,f=a.scaleY;return b(d)&&c.push("rotate("+d+"deg)"),b(e)&&b(f)&&c.push("scale("+e+","+f+")"),c.length?c.join(" "):"none"}function k(a,b){var c,d,e=ua(a.degree)%180,f=(e>90?180-e:e)*Math.PI/180,g=va(f),h=wa(f),i=a.width,j=a.height,k=a.aspectRatio;return b?(c=i/(h+g/k),d=c/k):(c=i*h+j*g,d=i*g+j*h),{width:c,height:d}}function l(c,d){var e,f,g,h=a("<canvas>")[0],i=h.getContext("2d"),j=0,l=0,m=d.naturalWidth,n=d.naturalHeight,o=d.rotate,p=d.scaleX,q=d.scaleY,r=b(p)&&b(q)&&(1!==p||1!==q),s=b(o)&&0!==o,t=s||r,u=m*ua(p||1),v=n*ua(q||1);return r&&(e=u/2,f=v/2),s&&(g=k({width:u,height:v,degree:o}),u=g.width,v=g.height,e=u/2,f=v/2),h.width=u,h.height=v,t&&(j=-m/2,l=-n/2,i.save(),i.translate(e,f)),s&&i.rotate(o*Math.PI/180),r&&i.scale(p,q),i.drawImage(c,za(j),za(l),za(m),za(n)),t&&i.restore(),h}function m(b){var c=b.length,d=0,e=0;return c&&(a.each(b,function(a,b){d+=b.pageX,e+=b.pageY}),d/=c,e/=c),{pageX:d,pageY:e}}function n(a,b,c){var d,e="";for(d=b,c+=b;c>d;d++)e+=Aa(a.getUint8(d));return e}function o(a){var b,c,d,e,f,g,h,i,j,k,l=new y(a),m=l.byteLength;if(255===l.getUint8(0)&&216===l.getUint8(1))for(j=2;m>j;){if(255===l.getUint8(j)&&225===l.getUint8(j+1)){h=j;break}j++}if(h&&(c=h+4,d=h+10,"Exif"===n(l,c,4)&&(g=l.getUint16(d),f=18761===g,(f||19789===g)&&42===l.getUint16(d+2,f)&&(e=l.getUint32(d+4,f),e>=8&&(i=d+e)))),i)for(m=l.getUint16(i,f),k=0;m>k;k++)if(j=i+12*k+2,274===l.getUint16(j,f)){j+=8,b=l.getUint16(j,f),qa&&l.setUint16(j,1,f);break}return b}function p(a){var b,c=a.replace($,""),d=atob(c),e=d.length,f=new w(e),g=new x(f);for(b=0;e>b;b++)g[b]=d.charCodeAt(b);return f}function q(a){var b,c=new x(a),d=c.length,e="";for(b=0;d>b;b++)e+=Aa(c[b]);return"data:image/jpeg;base64,"+z(e)}function r(b,c){this.$element=a(b),this.options=a.extend({},r.DEFAULTS,a.isPlainObject(c)&&c),this.isLoaded=!1,this.isBuilt=!1,this.isCompleted=!1,this.isRotated=!1,this.isCropped=!1,this.isDisabled=!1,this.isReplaced=!1,this.isLimited=!1,this.wheeling=!1,this.isImg=!1,this.originalUrl="",this.canvas=null,this.cropBox=null,this.init()}var s=a(window),t=a(document),u=window.location,v=window.navigator,w=window.ArrayBuffer,x=window.Uint8Array,y=window.DataView,z=window.btoa,A="cropper",B="cropper-modal",C="cropper-hide",D="cropper-hidden",E="cropper-invisible",F="cropper-move",G="cropper-crop",H="cropper-disabled",I="cropper-bg",J="mousedown touchstart pointerdown MSPointerDown",K="mousemove touchmove pointermove MSPointerMove",L="mouseup touchend touchcancel pointerup pointercancel MSPointerUp MSPointerCancel",M="wheel mousewheel DOMMouseScroll",N="dblclick",O="load."+A,P="error."+A,Q="resize."+A,R="build."+A,S="built."+A,T="cropstart."+A,U="cropmove."+A,V="cropend."+A,W="crop."+A,X="zoom."+A,Y=/e|w|s|n|se|sw|ne|nw|all|crop|move|zoom/,Z=/^data\:/,$=/^data\:([^\;]+)\;base64,/,_=/^data\:image\/jpeg.*;base64,/,aa="preview",ba="action",ca="e",da="w",ea="s",fa="n",ga="se",ha="sw",ia="ne",ja="nw",ka="all",la="crop",ma="move",na="zoom",oa="none",pa=a.isFunction(a("<canvas>")[0].getContext),qa=v&&/safari/i.test(v.userAgent)&&/apple computer/i.test(v.vendor),ra=Number,sa=Math.min,ta=Math.max,ua=Math.abs,va=Math.sin,wa=Math.cos,xa=Math.sqrt,ya=Math.round,za=Math.floor,Aa=String.fromCharCode;r.prototype={constructor:r,init:function(){var a,b=this.$element;if(b.is("img")){if(this.isImg=!0,this.originalUrl=a=b.attr("src"),!a)return;a=b.prop("src")}else b.is("canvas")&&pa&&(a=b[0].toDataURL());this.load(a)},trigger:function(b,c){var d=a.Event(b,c);return this.$element.trigger(d),d},load:function(b){var c,d,e=this.options,f=this.$element;if(b&&(f.one(R,e.build),!this.trigger(R).isDefaultPrevented())){if(this.url=b,this.image={},!e.checkOrientation||!w)return this.clone();if(c=a.proxy(this.read,this),Z.test(b))return _.test(b)?c(p(b)):this.clone();d=new XMLHttpRequest,d.onerror=d.onabort=a.proxy(function(){this.clone()},this),d.onload=function(){c(this.response)},d.open("get",b),d.responseType="arraybuffer",d.send()}},read:function(a){var b,c,d,e=this.options,f=o(a),g=this.image;if(f>1)switch(this.url=q(a),f){case 2:c=-1;break;case 3:b=-180;break;case 4:d=-1;break;case 5:b=90,d=-1;break;case 6:b=90;break;case 7:b=90,c=-1;break;case 8:b=-90}e.rotatable&&(g.rotate=b),e.scalable&&(g.scaleX=c,g.scaleY=d),this.clone()},clone:function(){var b,c,d=this.options,e=this.$element,i=this.url,j="";d.checkCrossOrigin&&f(i)&&(j=e.prop("crossOrigin"),j?b=i:(j="anonymous",b=g(i))),this.crossOrigin=j,this.crossOriginUrl=b,this.$clone=c=a("<img"+h(j)+' src="'+(b||i)+'">'),this.isImg?e[0].complete?this.start():e.one(O,a.proxy(this.start,this)):c.one(O,a.proxy(this.start,this)).one(P,a.proxy(this.stop,this)).addClass(C).insertAfter(e)},start:function(){var b=this.$element,c=this.$clone;this.isImg||(c.off(P,this.stop),b=c),i(b[0],a.proxy(function(b,c){a.extend(this.image,{naturalWidth:b,naturalHeight:c,aspectRatio:b/c}),this.isLoaded=!0,this.build()},this))},stop:function(){this.$clone.remove(),this.$clone=null},build:function(){var b,c,d,e=this.options,f=this.$element,g=this.$clone;this.isLoaded&&(this.isBuilt&&this.unbuild(),this.$container=f.parent(),this.$cropper=b=a(r.TEMPLATE),this.$canvas=b.find(".cropper-canvas").append(g),this.$dragBox=b.find(".cropper-drag-box"),this.$cropBox=c=b.find(".cropper-crop-box"),this.$viewBox=b.find(".cropper-view-box"),this.$face=d=c.find(".cropper-face"),f.addClass(D).after(b),this.isImg||g.removeClass(C),this.initPreview(),this.bind(),e.aspectRatio=ta(0,e.aspectRatio)||NaN,e.viewMode=ta(0,sa(3,ya(e.viewMode)))||0,e.autoCrop?(this.isCropped=!0,e.modal&&this.$dragBox.addClass(B)):c.addClass(D),e.guides||c.find(".cropper-dashed").addClass(D),e.center||c.find(".cropper-center").addClass(D),e.cropBoxMovable&&d.addClass(F).data(ba,ka),e.highlight||d.addClass(E),e.background&&b.addClass(I),e.cropBoxResizable||c.find(".cropper-line, .cropper-point").addClass(D),this.setDragMode(e.dragMode),this.render(),this.isBuilt=!0,this.setData(e.data),f.one(S,e.built),setTimeout(a.proxy(function(){this.trigger(S),this.isCompleted=!0},this),0))},unbuild:function(){this.isBuilt&&(this.isBuilt=!1,this.isCompleted=!1,this.initialImage=null,this.initialCanvas=null,this.initialCropBox=null,this.container=null,this.canvas=null,this.cropBox=null,this.unbind(),this.resetPreview(),this.$preview=null,this.$viewBox=null,this.$cropBox=null,this.$dragBox=null,this.$canvas=null,this.$container=null,this.$cropper.remove(),this.$cropper=null)},render:function(){this.initContainer(),this.initCanvas(),this.initCropBox(),this.renderCanvas(),this.isCropped&&this.renderCropBox()},initContainer:function(){var a=this.options,b=this.$element,c=this.$container,d=this.$cropper;d.addClass(D),b.removeClass(D),d.css(this.container={width:ta(c.width(),ra(a.minContainerWidth)||200),height:ta(c.height(),ra(a.minContainerHeight)||100)}),b.addClass(D),d.removeClass(D)},initCanvas:function(){var b,c=this.options.viewMode,d=this.container,e=d.width,f=d.height,g=this.image,h=g.naturalWidth,i=g.naturalHeight,j=90===ua(g.rotate),k=j?i:h,l=j?h:i,m=k/l,n=e,o=f;f*m>e?3===c?n=f*m:o=e/m:3===c?o=e/m:n=f*m,b={naturalWidth:k,naturalHeight:l,aspectRatio:m,width:n,height:o},b.oldLeft=b.left=(e-n)/2,b.oldTop=b.top=(f-o)/2,this.canvas=b,this.isLimited=1===c||2===c,this.limitCanvas(!0,!0),this.initialImage=a.extend({},g),this.initialCanvas=a.extend({},b)},limitCanvas:function(a,b){var c,d,e,f,g=this.options,h=g.viewMode,i=this.container,j=i.width,k=i.height,l=this.canvas,m=l.aspectRatio,n=this.cropBox,o=this.isCropped&&n;a&&(c=ra(g.minCanvasWidth)||0,d=ra(g.minCanvasHeight)||0,h&&(h>1?(c=ta(c,j),d=ta(d,k),3===h&&(d*m>c?c=d*m:d=c/m)):c?c=ta(c,o?n.width:0):d?d=ta(d,o?n.height:0):o&&(c=n.width,d=n.height,d*m>c?c=d*m:d=c/m)),c&&d?d*m>c?d=c/m:c=d*m:c?d=c/m:d&&(c=d*m),l.minWidth=c,l.minHeight=d,l.maxWidth=1/0,l.maxHeight=1/0),b&&(h?(e=j-l.width,f=k-l.height,l.minLeft=sa(0,e),l.minTop=sa(0,f),l.maxLeft=ta(0,e),l.maxTop=ta(0,f),o&&this.isLimited&&(l.minLeft=sa(n.left,n.left+n.width-l.width),l.minTop=sa(n.top,n.top+n.height-l.height),l.maxLeft=n.left,l.maxTop=n.top,2===h&&(l.width>=j&&(l.minLeft=sa(0,e),l.maxLeft=ta(0,e)),l.height>=k&&(l.minTop=sa(0,f),l.maxTop=ta(0,f))))):(l.minLeft=-l.width,l.minTop=-l.height,l.maxLeft=j,l.maxTop=k))},renderCanvas:function(a){var b,c,d=this.canvas,e=this.image,f=e.rotate,g=e.naturalWidth,h=e.naturalHeight;this.isRotated&&(this.isRotated=!1,c=k({width:e.width,height:e.height,degree:f}),b=c.width/c.height,b!==d.aspectRatio&&(d.left-=(c.width-d.width)/2,d.top-=(c.height-d.height)/2,d.width=c.width,d.height=c.height,d.aspectRatio=b,d.naturalWidth=g,d.naturalHeight=h,f%180&&(c=k({width:g,height:h,degree:f}),d.naturalWidth=c.width,d.naturalHeight=c.height),this.limitCanvas(!0,!1))),(d.width>d.maxWidth||d.width<d.minWidth)&&(d.left=d.oldLeft),(d.height>d.maxHeight||d.height<d.minHeight)&&(d.top=d.oldTop),d.width=sa(ta(d.width,d.minWidth),d.maxWidth),d.height=sa(ta(d.height,d.minHeight),d.maxHeight),this.limitCanvas(!1,!0),d.oldLeft=d.left=sa(ta(d.left,d.minLeft),d.maxLeft),d.oldTop=d.top=sa(ta(d.top,d.minTop),d.maxTop),this.$canvas.css({width:d.width,height:d.height,left:d.left,top:d.top}),this.renderImage(),this.isCropped&&this.isLimited&&this.limitCropBox(!0,!0),a&&this.output()},renderImage:function(b){var c,d=this.canvas,e=this.image;e.rotate&&(c=k({width:d.width,height:d.height,degree:e.rotate,aspectRatio:e.aspectRatio},!0)),a.extend(e,c?{width:c.width,height:c.height,left:(d.width-c.width)/2,top:(d.height-c.height)/2}:{width:d.width,height:d.height,left:0,top:0}),this.$clone.css({width:e.width,height:e.height,marginLeft:e.left,marginTop:e.top,transform:j(e)}),b&&this.output()},initCropBox:function(){var b=this.options,c=this.canvas,d=b.aspectRatio,e=ra(b.autoCropArea)||.8,f={width:c.width,height:c.height};d&&(c.height*d>c.width?f.height=f.width/d:f.width=f.height*d),this.cropBox=f,this.limitCropBox(!0,!0),f.width=sa(ta(f.width,f.minWidth),f.maxWidth),f.height=sa(ta(f.height,f.minHeight),f.maxHeight),f.width=ta(f.minWidth,f.width*e),f.height=ta(f.minHeight,f.height*e),f.oldLeft=f.left=c.left+(c.width-f.width)/2,f.oldTop=f.top=c.top+(c.height-f.height)/2,this.initialCropBox=a.extend({},f)},limitCropBox:function(a,b){var c,d,e,f,g=this.options,h=g.aspectRatio,i=this.container,j=i.width,k=i.height,l=this.canvas,m=this.cropBox,n=this.isLimited;a&&(c=ra(g.minCropBoxWidth)||0,d=ra(g.minCropBoxHeight)||0,c=sa(c,j),d=sa(d,k),e=sa(j,n?l.width:j),f=sa(k,n?l.height:k),h&&(c&&d?d*h>c?d=c/h:c=d*h:c?d=c/h:d&&(c=d*h),f*h>e?f=e/h:e=f*h),m.minWidth=sa(c,e),m.minHeight=sa(d,f),m.maxWidth=e,m.maxHeight=f),b&&(n?(m.minLeft=ta(0,l.left),m.minTop=ta(0,l.top),m.maxLeft=sa(j,l.left+l.width)-m.width,m.maxTop=sa(k,l.top+l.height)-m.height):(m.minLeft=0,m.minTop=0,m.maxLeft=j-m.width,m.maxTop=k-m.height))},renderCropBox:function(){var a=this.options,b=this.container,c=b.width,d=b.height,e=this.cropBox;(e.width>e.maxWidth||e.width<e.minWidth)&&(e.left=e.oldLeft),(e.height>e.maxHeight||e.height<e.minHeight)&&(e.top=e.oldTop),e.width=sa(ta(e.width,e.minWidth),e.maxWidth),e.height=sa(ta(e.height,e.minHeight),e.maxHeight),this.limitCropBox(!1,!0),e.oldLeft=e.left=sa(ta(e.left,e.minLeft),e.maxLeft),e.oldTop=e.top=sa(ta(e.top,e.minTop),e.maxTop),a.movable&&a.cropBoxMovable&&this.$face.data(ba,e.width===c&&e.height===d?ma:ka),this.$cropBox.css({width:e.width,height:e.height,left:e.left,top:e.top}),this.isCropped&&this.isLimited&&this.limitCanvas(!0,!0),this.isDisabled||this.output()},output:function(){this.preview(),this.isCompleted?this.trigger(W,this.getData()):this.isBuilt||this.$element.one(S,a.proxy(function(){this.trigger(W,this.getData())},this))},initPreview:function(){var b,c=h(this.crossOrigin),d=c?this.crossOriginUrl:this.url;this.$preview=a(this.options.preview),this.$clone2=b=a("<img"+c+' src="'+d+'">'),this.$viewBox.html(b),this.$preview.each(function(){var b=a(this);b.data(aa,{width:b.width(),height:b.height(),html:b.html()}),b.html("<img"+c+' src="'+d+'" style="display:block;width:100%;height:auto;min-width:0!important;min-height:0!important;max-width:none!important;max-height:none!important;image-orientation:0deg!important;">')})},resetPreview:function(){this.$preview.each(function(){var b=a(this),c=b.data(aa);b.css({width:c.width,height:c.height}).html(c.html).removeData(aa)})},preview:function(){var b=this.image,c=this.canvas,d=this.cropBox,e=d.width,f=d.height,g=b.width,h=b.height,i=d.left-c.left-b.left,k=d.top-c.top-b.top;this.isCropped&&!this.isDisabled&&(this.$clone2.css({width:g,height:h,marginLeft:-i,marginTop:-k,transform:j(b)}),this.$preview.each(function(){var c=a(this),d=c.data(aa),l=d.width,m=d.height,n=l,o=m,p=1;e&&(p=l/e,o=f*p),f&&o>m&&(p=m/f,n=e*p,o=m),c.css({width:n,height:o}).find("img").css({width:g*p,height:h*p,marginLeft:-i*p,marginTop:-k*p,transform:j(b)})}))},bind:function(){var b=this.options,c=this.$element,d=this.$cropper;a.isFunction(b.cropstart)&&c.on(T,b.cropstart),a.isFunction(b.cropmove)&&c.on(U,b.cropmove),a.isFunction(b.cropend)&&c.on(V,b.cropend),a.isFunction(b.crop)&&c.on(W,b.crop),a.isFunction(b.zoom)&&c.on(X,b.zoom),d.on(J,a.proxy(this.cropStart,this)),b.zoomable&&b.zoomOnWheel&&d.on(M,a.proxy(this.wheel,this)),b.toggleDragModeOnDblclick&&d.on(N,a.proxy(this.dblclick,this)),t.on(K,this._cropMove=e(this.cropMove,this)).on(L,this._cropEnd=e(this.cropEnd,this)),b.responsive&&s.on(Q,this._resize=e(this.resize,this))},unbind:function(){var b=this.options,c=this.$element,d=this.$cropper;a.isFunction(b.cropstart)&&c.off(T,b.cropstart),a.isFunction(b.cropmove)&&c.off(U,b.cropmove),a.isFunction(b.cropend)&&c.off(V,b.cropend),a.isFunction(b.crop)&&c.off(W,b.crop),a.isFunction(b.zoom)&&c.off(X,b.zoom),d.off(J,this.cropStart),b.zoomable&&b.zoomOnWheel&&d.off(M,this.wheel),b.toggleDragModeOnDblclick&&d.off(N,this.dblclick),t.off(K,this._cropMove).off(L,this._cropEnd),b.responsive&&s.off(Q,this._resize)},resize:function(){var b,c,d,e=this.options.restore,f=this.$container,g=this.container;!this.isDisabled&&g&&(d=f.width()/g.width,1===d&&f.height()===g.height||(e&&(b=this.getCanvasData(),c=this.getCropBoxData()),this.render(),e&&(this.setCanvasData(a.each(b,function(a,c){b[a]=c*d})),this.setCropBoxData(a.each(c,function(a,b){c[a]=b*d})))))},dblclick:function(){this.isDisabled||(this.$dragBox.hasClass(G)?this.setDragMode(ma):this.setDragMode(la))},wheel:function(b){var c=b.originalEvent||b,d=ra(this.options.wheelZoomRatio)||.1,e=1;this.isDisabled||(b.preventDefault(),this.wheeling||(this.wheeling=!0,setTimeout(a.proxy(function(){this.wheeling=!1},this),50),c.deltaY?e=c.deltaY>0?1:-1:c.wheelDelta?e=-c.wheelDelta/120:c.detail&&(e=c.detail>0?1:-1),this.zoom(-e*d,b)))},cropStart:function(b){var c,d,e=this.options,f=b.originalEvent,g=f&&f.touches,h=b;if(!this.isDisabled){if(g){if(c=g.length,c>1){if(!e.zoomable||!e.zoomOnTouch||2!==c)return;h=g[1],this.startX2=h.pageX,this.startY2=h.pageY,d=na}h=g[0]}if(d=d||a(h.target).data(ba),Y.test(d)){if(this.trigger(T,{originalEvent:f,action:d}).isDefaultPrevented())return;b.preventDefault(),this.action=d,this.cropping=!1,this.startX=h.pageX||f&&f.pageX,this.startY=h.pageY||f&&f.pageY,d===la&&(this.cropping=!0,this.$dragBox.addClass(B))}}},cropMove:function(a){var b,c=this.options,d=a.originalEvent,e=d&&d.touches,f=a,g=this.action;if(!this.isDisabled){if(e){if(b=e.length,b>1){if(!c.zoomable||!c.zoomOnTouch||2!==b)return;f=e[1],this.endX2=f.pageX,this.endY2=f.pageY}f=e[0]}if(g){if(this.trigger(U,{originalEvent:d,action:g}).isDefaultPrevented())return;a.preventDefault(),this.endX=f.pageX||d&&d.pageX,this.endY=f.pageY||d&&d.pageY,this.change(f.shiftKey,g===na?a:null)}}},cropEnd:function(a){var b=a.originalEvent,c=this.action;this.isDisabled||c&&(a.preventDefault(),this.cropping&&(this.cropping=!1,this.$dragBox.toggleClass(B,this.isCropped&&this.options.modal)),this.action="",this.trigger(V,{originalEvent:b,action:c}))},change:function(a,b){var c,d,e=this.options,f=e.aspectRatio,g=this.action,h=this.container,i=this.canvas,j=this.cropBox,k=j.width,l=j.height,m=j.left,n=j.top,o=m+k,p=n+l,q=0,r=0,s=h.width,t=h.height,u=!0;switch(!f&&a&&(f=k&&l?k/l:1),this.limited&&(q=j.minLeft,r=j.minTop,s=q+sa(h.width,i.left+i.width),t=r+sa(h.height,i.top+i.height)),d={x:this.endX-this.startX,y:this.endY-this.startY},f&&(d.X=d.y*f,d.Y=d.x/f),g){case ka:m+=d.x,n+=d.y;break;case ca:if(d.x>=0&&(o>=s||f&&(r>=n||p>=t))){u=!1;break}k+=d.x,f&&(l=k/f,n-=d.Y/2),0>k&&(g=da,k=0);break;case fa:if(d.y<=0&&(r>=n||f&&(q>=m||o>=s))){u=!1;break}l-=d.y,n+=d.y,f&&(k=l*f,m+=d.X/2),0>l&&(g=ea,l=0);break;case da:if(d.x<=0&&(q>=m||f&&(r>=n||p>=t))){u=!1;break}k-=d.x,m+=d.x,f&&(l=k/f,n+=d.Y/2),0>k&&(g=ca,k=0);break;case ea:if(d.y>=0&&(p>=t||f&&(q>=m||o>=s))){u=!1;break}l+=d.y,f&&(k=l*f,m-=d.X/2),0>l&&(g=fa,l=0);break;case ia:if(f){if(d.y<=0&&(r>=n||o>=s)){u=!1;break}l-=d.y,n+=d.y,k=l*f}else d.x>=0?s>o?k+=d.x:d.y<=0&&r>=n&&(u=!1):k+=d.x,d.y<=0?n>r&&(l-=d.y,n+=d.y):(l-=d.y,n+=d.y);0>k&&0>l?(g=ha,l=0,k=0):0>k?(g=ja,k=0):0>l&&(g=ga,l=0);break;case ja:if(f){if(d.y<=0&&(r>=n||q>=m)){u=!1;break}l-=d.y,n+=d.y,k=l*f,m+=d.X}else d.x<=0?m>q?(k-=d.x,m+=d.x):d.y<=0&&r>=n&&(u=!1):(k-=d.x,m+=d.x),d.y<=0?n>r&&(l-=d.y,n+=d.y):(l-=d.y,n+=d.y);0>k&&0>l?(g=ga,l=0,k=0):0>k?(g=ia,k=0):0>l&&(g=ha,l=0);break;case ha:if(f){if(d.x<=0&&(q>=m||p>=t)){u=!1;break}k-=d.x,m+=d.x,l=k/f}else d.x<=0?m>q?(k-=d.x,m+=d.x):d.y>=0&&p>=t&&(u=!1):(k-=d.x,m+=d.x),d.y>=0?t>p&&(l+=d.y):l+=d.y;0>k&&0>l?(g=ia,l=0,k=0):0>k?(g=ga,k=0):0>l&&(g=ja,l=0);break;case ga:if(f){if(d.x>=0&&(o>=s||p>=t)){u=!1;break}k+=d.x,l=k/f}else d.x>=0?s>o?k+=d.x:d.y>=0&&p>=t&&(u=!1):k+=d.x,d.y>=0?t>p&&(l+=d.y):l+=d.y;0>k&&0>l?(g=ja,l=0,k=0):0>k?(g=ha,k=0):0>l&&(g=ia,l=0);break;case ma:this.move(d.x,d.y),u=!1;break;case na:this.zoom(function(a,b,c,d){var e=xa(a*a+b*b),f=xa(c*c+d*d);return(f-e)/e}(ua(this.startX-this.startX2),ua(this.startY-this.startY2),ua(this.endX-this.endX2),ua(this.endY-this.endY2)),b),this.startX2=this.endX2,this.startY2=this.endY2,u=!1;break;case la:if(!d.x||!d.y){u=!1;break}c=this.$cropper.offset(),m=this.startX-c.left,n=this.startY-c.top,k=j.minWidth,l=j.minHeight,d.x>0?g=d.y>0?ga:ia:d.x<0&&(m-=k,g=d.y>0?ha:ja),d.y<0&&(n-=l),this.isCropped||(this.$cropBox.removeClass(D),this.isCropped=!0,this.limited&&this.limitCropBox(!0,!0))}u&&(j.width=k,j.height=l,j.left=m,j.top=n,this.action=g,this.renderCropBox()),this.startX=this.endX,this.startY=this.endY},crop:function(){this.isBuilt&&!this.isDisabled&&(this.isCropped||(this.isCropped=!0,this.limitCropBox(!0,!0),this.options.modal&&this.$dragBox.addClass(B),this.$cropBox.removeClass(D)),this.setCropBoxData(this.initialCropBox))},reset:function(){this.isBuilt&&!this.isDisabled&&(this.image=a.extend({},this.initialImage),this.canvas=a.extend({},this.initialCanvas),this.cropBox=a.extend({},this.initialCropBox),this.renderCanvas(),this.isCropped&&this.renderCropBox())},clear:function(){this.isCropped&&!this.isDisabled&&(a.extend(this.cropBox,{left:0,top:0,width:0,height:0}),this.isCropped=!1,this.renderCropBox(),this.limitCanvas(!0,!0),this.renderCanvas(),this.$dragBox.removeClass(B),this.$cropBox.addClass(D))},replace:function(a,b){!this.isDisabled&&a&&(this.isImg&&this.$element.attr("src",a),b?(this.url=a,this.$clone.attr("src",a),this.isBuilt&&this.$preview.find("img").add(this.$clone2).attr("src",a)):(this.isImg&&(this.isReplaced=!0),this.options.data=null,this.load(a)))},enable:function(){this.isBuilt&&(this.isDisabled=!1,this.$cropper.removeClass(H))},disable:function(){this.isBuilt&&(this.isDisabled=!0,this.$cropper.addClass(H))},destroy:function(){var a=this.$element;this.isLoaded?(this.isImg&&this.isReplaced&&a.attr("src",this.originalUrl),this.unbuild(),a.removeClass(D)):this.isImg?a.off(O,this.start):this.$clone&&this.$clone.remove(),a.removeData(A)},move:function(a,b){var d=this.canvas;this.moveTo(c(a)?a:d.left+ra(a),c(b)?b:d.top+ra(b))},moveTo:function(a,d){var e=this.canvas,f=!1;c(d)&&(d=a),a=ra(a),d=ra(d),this.isBuilt&&!this.isDisabled&&this.options.movable&&(b(a)&&(e.left=a,f=!0),b(d)&&(e.top=d,f=!0),f&&this.renderCanvas(!0))},zoom:function(a,b){var c=this.canvas;a=ra(a),a=0>a?1/(1-a):1+a,this.zoomTo(c.width*a/c.naturalWidth,b)},zoomTo:function(a,b){var c,d,e,f,g,h=this.options,i=this.canvas,j=i.width,k=i.height,l=i.naturalWidth,n=i.naturalHeight;if(a=ra(a),a>=0&&this.isBuilt&&!this.isDisabled&&h.zoomable){if(d=l*a,e=n*a,b&&(c=b.originalEvent),this.trigger(X,{originalEvent:c,oldRatio:j/l,ratio:d/l}).isDefaultPrevented())return;c?(f=this.$cropper.offset(),g=c.touches?m(c.touches):{pageX:b.pageX||c.pageX||0,pageY:b.pageY||c.pageY||0},i.left-=(d-j)*((g.pageX-f.left-i.left)/j),i.top-=(e-k)*((g.pageY-f.top-i.top)/k)):(i.left-=(d-j)/2,i.top-=(e-k)/2),i.width=d,i.height=e,this.renderCanvas(!0)}},rotate:function(a){this.rotateTo((this.image.rotate||0)+ra(a))},rotateTo:function(a){a=ra(a),b(a)&&this.isBuilt&&!this.isDisabled&&this.options.rotatable&&(this.image.rotate=a%360,this.isRotated=!0,this.renderCanvas(!0))},scale:function(a,d){var e=this.image,f=!1;c(d)&&(d=a),a=ra(a),d=ra(d),this.isBuilt&&!this.isDisabled&&this.options.scalable&&(b(a)&&(e.scaleX=a,f=!0),b(d)&&(e.scaleY=d,f=!0),f&&this.renderImage(!0))},scaleX:function(a){var c=this.image.scaleY;this.scale(a,b(c)?c:1)},scaleY:function(a){var c=this.image.scaleX;this.scale(b(c)?c:1,a)},getData:function(b){var c,d,e=this.options,f=this.image,g=this.canvas,h=this.cropBox;return this.isBuilt&&this.isCropped?(d={x:h.left-g.left,y:h.top-g.top,width:h.width,height:h.height},c=f.width/f.naturalWidth,a.each(d,function(a,e){e/=c,d[a]=b?ya(e):e})):d={x:0,y:0,width:0,height:0},e.rotatable&&(d.rotate=f.rotate||0),e.scalable&&(d.scaleX=f.scaleX||1,d.scaleY=f.scaleY||1),d},setData:function(c){var d,e,f,g=this.options,h=this.image,i=this.canvas,j={};a.isFunction(c)&&(c=c.call(this.element)),this.isBuilt&&!this.isDisabled&&a.isPlainObject(c)&&(g.rotatable&&b(c.rotate)&&c.rotate!==h.rotate&&(h.rotate=c.rotate,this.isRotated=d=!0),g.scalable&&(b(c.scaleX)&&c.scaleX!==h.scaleX&&(h.scaleX=c.scaleX,e=!0),b(c.scaleY)&&c.scaleY!==h.scaleY&&(h.scaleY=c.scaleY,e=!0)),d?this.renderCanvas():e&&this.renderImage(),f=h.width/h.naturalWidth,b(c.x)&&(j.left=c.x*f+i.left),b(c.y)&&(j.top=c.y*f+i.top),b(c.width)&&(j.width=c.width*f),b(c.height)&&(j.height=c.height*f),this.setCropBoxData(j))},getContainerData:function(){return this.isBuilt?this.container:{}},getImageData:function(){return this.isLoaded?this.image:{}},getCanvasData:function(){var b=this.canvas,c={};return this.isBuilt&&a.each(["left","top","width","height","naturalWidth","naturalHeight"],function(a,d){c[d]=b[d]}),c},setCanvasData:function(c){var d=this.canvas,e=d.aspectRatio;a.isFunction(c)&&(c=c.call(this.$element)),this.isBuilt&&!this.isDisabled&&a.isPlainObject(c)&&(b(c.left)&&(d.left=c.left),b(c.top)&&(d.top=c.top),b(c.width)?(d.width=c.width,d.height=c.width/e):b(c.height)&&(d.height=c.height,d.width=c.height*e),this.renderCanvas(!0))},getCropBoxData:function(){var a,b=this.cropBox;return this.isBuilt&&this.isCropped&&(a={left:b.left,top:b.top,width:b.width,height:b.height}),a||{}},setCropBoxData:function(c){var d,e,f=this.cropBox,g=this.options.aspectRatio;a.isFunction(c)&&(c=c.call(this.$element)),this.isBuilt&&this.isCropped&&!this.isDisabled&&a.isPlainObject(c)&&(b(c.left)&&(f.left=c.left),b(c.top)&&(f.top=c.top),b(c.width)&&(d=!0,f.width=c.width),b(c.height)&&(e=!0,f.height=c.height),g&&(d?f.height=f.width/g:e&&(f.width=f.height*g)),this.renderCropBox())},getCroppedCanvas:function(b){var c,d,e,f,g,h,i,j,k,m,n;return this.isBuilt&&this.isCropped&&pa?(a.isPlainObject(b)||(b={}),n=this.getData(),c=n.width,d=n.height,j=c/d,a.isPlainObject(b)&&(g=b.width,h=b.height,g?(h=g/j,i=g/c):h&&(g=h*j,i=h/d)),e=za(g||c),f=za(h||d),k=a("<canvas>")[0],k.width=e,k.height=f,m=k.getContext("2d"),b.fillColor&&(m.fillStyle=b.fillColor,m.fillRect(0,0,e,f)),m.drawImage.apply(m,function(){var a,b,e,f,g,h,j=l(this.$clone[0],this.image),k=j.width,m=j.height,o=this.canvas,p=[j],q=n.x+o.naturalWidth*(ua(n.scaleX||1)-1)/2,r=n.y+o.naturalHeight*(ua(n.scaleY||1)-1)/2;return-c>=q||q>k?q=a=e=g=0:0>=q?(e=-q,q=0,a=g=sa(k,c+q)):k>=q&&(e=0,a=g=sa(c,k-q)),0>=a||-d>=r||r>m?r=b=f=h=0:0>=r?(f=-r,r=0,b=h=sa(m,d+r)):m>=r&&(f=0,b=h=sa(d,m-r)),p.push(za(q),za(r),za(a),za(b)),i&&(e*=i,f*=i,g*=i,h*=i),g>0&&h>0&&p.push(za(e),za(f),za(g),za(h)),p}.call(this)),k):void 0},setAspectRatio:function(a){var b=this.options;this.isDisabled||c(a)||(b.aspectRatio=ta(0,a)||NaN,this.isBuilt&&(this.initCropBox(),this.isCropped&&this.renderCropBox()))},setDragMode:function(a){var b,c,d=this.options;this.isLoaded&&!this.isDisabled&&(b=a===la,c=d.movable&&a===ma,a=b||c?a:oa,this.$dragBox.data(ba,a).toggleClass(G,b).toggleClass(F,c),d.cropBoxMovable||this.$face.data(ba,a).toggleClass(G,b).toggleClass(F,c))}},r.DEFAULTS={viewMode:0,dragMode:"crop",aspectRatio:NaN,data:null,preview:"",responsive:!0,restore:!0,checkCrossOrigin:!0,checkOrientation:!0,modal:!0,guides:!0,center:!0,highlight:!0,background:!0,autoCrop:!0,autoCropArea:.8,movable:!0,rotatable:!0,scalable:!0,zoomable:!0,zoomOnTouch:!0,zoomOnWheel:!0,wheelZoomRatio:.1,cropBoxMovable:!0,cropBoxResizable:!0,toggleDragModeOnDblclick:!0,minCanvasWidth:0,minCanvasHeight:0,minCropBoxWidth:0,minCropBoxHeight:0,minContainerWidth:200,minContainerHeight:100,build:null,built:null,cropstart:null,cropmove:null,cropend:null,crop:null,zoom:null},r.setDefaults=function(b){a.extend(r.DEFAULTS,b)},r.TEMPLATE='<div class="cropper-container"><div class="cropper-wrap-box"><div class="cropper-canvas"></div></div><div class="cropper-drag-box"></div><div class="cropper-crop-box"><span class="cropper-view-box"></span><span class="cropper-dashed dashed-h"></span><span class="cropper-dashed dashed-v"></span><span class="cropper-center"></span><span class="cropper-face"></span><span class="cropper-line line-e" data-action="e"></span><span class="cropper-line line-n" data-action="n"></span><span class="cropper-line line-w" data-action="w"></span><span class="cropper-line line-s" data-action="s"></span><span class="cropper-point point-e" data-action="e"></span><span class="cropper-point point-n" data-action="n"></span><span class="cropper-point point-w" data-action="w"></span><span class="cropper-point point-s" data-action="s"></span><span class="cropper-point point-ne" data-action="ne"></span><span class="cropper-point point-nw" data-action="nw"></span><span class="cropper-point point-sw" data-action="sw"></span><span class="cropper-point point-se" data-action="se"></span></div></div>',r.other=a.fn.cropper,a.fn.cropper=function(b){var e,f=d(arguments,1);return this.each(function(){var c,d,g=a(this),h=g.data(A);if(!h){if(/destroy/.test(b))return;c=a.extend({},g.data(),a.isPlainObject(b)&&b),g.data(A,h=new r(this,c))}"string"==typeof b&&a.isFunction(d=h[b])&&(e=d.apply(h,f))}),c(e)?this:e},a.fn.cropper.Constructor=r,a.fn.cropper.setDefaults=r.setDefaults,a.fn.cropper.noConflict=function(){return a.fn.cropper=r.other,this}}),require(["pat-base","jquery","plone_app_imagecropping_cropper"],function(a,b){"use strict";var c=a.extend({name:"image-cropper",trigger:".pat-image-cropper",parser:"mockup",while_reset:!1,while_init:!0,while_saving:!1,_changed:!1,defaults:{identifier:null,fieldname:null,saveurl:null,authenticator:null,scale:null,preview:null,is_cropped:null,view_mode:3,aspect_ratio:16/9,currrent_x:null,currrent_y:null,currrent_w:null,currrent_h:null,true_width:null,true_height:null},update_badges:function(){return this.while_saving?(this.$badge_saving.show(),this.$button_save.prop("disabled",!0),this.$button_reset.prop("disabled",!0),void this.$button_remove.prop("disabled",!0)):(this.$badge_saving.hide(),this.options.is_cropped?(this.$button_remove.prop("disabled",!1),this.$badge_uncropped.hide(),this.$badge_cropped.show()):(this.$button_remove.prop("disabled",!0),this.$badge_uncropped.show(),this.$badge_cropped.hide()),void(this.crop_changed()?(this.$badge_changed.show(),this.$button_save.prop("disabled",!1),this.$button_reset.prop("disabled",!1)):(this.$badge_changed.hide(),this.options.is_cropped?(this.$button_save.prop("disabled",!0),this.$button_reset.prop("disabled",!0)):(this.$button_save.prop("disabled",!1),this.$button_reset.prop("disabled",!0)))))},crop_changed:function(){if(this.while_init||this.while_reset)return!1;if(!b(".cropper-container",this.$image.parent()).is(":visible"))return this._changed;var a=this.$image.cropper("getData"),c=this.original_data.x-1<a.x&&a.x<this.original_data.x+1,d=this.original_data.y-1<a.y&&a.y<this.original_data.y+1,e=this.original_data.width-1<a.width&&a.width<this.original_data.width+1,f=this.original_data.height-1<a.height&&a.height<this.original_data.height+1;return this._changed=!(c&&d&&e&&f),this._changed},reset:function(){console.log("RESET"),this.while_reset=!0,this.cropper.setData(this.original_data),this.visualize_selected_area(),this.while_reset=!1,this.update_badges()},remove:function(){console.log("REMOVE");var a=this,c={remove:!0,fieldname:this.options.fieldname,scale:this.options.scalename,_authenticator:this.options.authenticator};a.while_saving=!0,a.update_badges(),b.ajax({url:this.options.saveurl,type:"POST",data:c,success:function(b,c,d){a.options.is_cropped=!1,a.while_saving=!1,a.update_badges()},error:function(b,c,d){a.while_saving=!1,a.update_badges(),alert(c,d)}})},save:function(){console.log("SAVE "+this.identifier);var a=this,c=this.$image.cropper("getData"),d={x:c.x,y:c.y,width:c.width,height:c.height,fieldname:this.options.fieldname,scale:this.options.scalename,_authenticator:this.options.authenticator};a.while_saving=!0,a.update_badges(),b.ajax({url:this.options.saveurl,type:"POST",data:d,success:function(c,d,e){a.options.is_cropped=!0,a._changed=!1,a.original_data=b.extend({},a.cropper.getData()),a.while_saving=!1,a.update_badges()},error:function(b,c,d){a.while_saving=!1,a.update_badges(),alert(c,d)}})},visualize_selected_area:function(){var a=this.$image.cropper("getData");b(".cropx",self.$el).text(Math.round(a.x)),b(".cropy",self.$el).text(Math.round(a.y)),b(".cropw",self.$el).text(Math.round(a.width)),b(".croph",self.$el).text(Math.round(a.height))},notify_visible:function(){this.while_reset=!0,this.cropper.resize(),this.options.is_cropped&&!this.crop_changed()&&(console.log("set to orig"),this.cropper.setData(this.original_data),this.visualize_selected_area()),this.while_reset=!1},limit_minimum_cropping_size:function(){var a=this.$image.cropper("getData"),b={};(a.width<this.options.target_width||a.height<this.options.target_height)&&(b.width=this.options.target_width,b.height=this.options.target_height,a.x+this.options.target_width>this.options.true_width?b.x=this.options.true_width-this.options.target_width:b.x=a.x,a.y+this.options.target_height>this.options.true_height?b.y=this.options.true_height-this.options.target_height:b.y=a.y,b.rotate=a.rotate,b.scaleX=a.scaleX,b.scaleY=a.scaleY,this.while_reset=!0,this.cropper.setData(b),this.while_reset=!1)},init:function(){var a=this,c=(a.$el.parent().hasClass("inactive"),"#select-"+a.options.identifier),d=("#croppingarea-"+a.options.identifier,"#croppingarea-"+a.options.identifier);a.identifier=a.options.identifier,a.$image=b("img.main-image",a.$el),a.$badge_cropped=b(c+" .label.cropped"),
a.$badge_uncropped=b(c+" .label.uncropped"),a.$badge_changed=b(c+" .label.changed"),a.$badge_saving=b(c+" .label.saving"),a.$button_save=b(d+" button.save"),a.$button_remove=b(d+" button.remove"),a.$button_reset=b(d+" button.reset"),a.$button_save_all=b("button.save-all"),a.options.current_x=parseFloat(a.options.current_x),a.options.current_y=parseFloat(a.options.current_y),a.options.current_w=parseFloat(a.options.current_w),a.options.current_h=parseFloat(a.options.current_h),a.options.true_width=parseFloat(a.options.true_width),a.options.true_height=parseFloat(a.options.true_height),a.options.target_width=parseFloat(a.options.target_width),a.options.target_height=parseFloat(a.options.target_height),a.options.is_cropped="True"==a.options.is_cropped,a.original_data={x:this.options.current_x,y:this.options.current_y,width:this.options.current_w,height:this.options.current_h,rotate:0,scaleX:1,scaleY:1},a.update_badges(),a.$button_reset.click(function(){a.reset()}),a.$button_remove.click(function(){a.remove()}),a.$button_save.click(function(){a.save()}),a.$button_save_all.on("click",{identifier:a.identifier},function(b){a.crop_changed()&&a.save()});var e={preview:a.options.preview,data:a.original_data,autoCrop:!0,autoCropArea:1,aspectRatio:parseFloat(a.options.aspect_ratio),viewMode:a.options.view_mode,restore:!1,crop:function(b){a.while_init||a.while_reset||(a.limit_minimum_cropping_size(),a.update_badges(),a.visualize_selected_area())},built:function(){a.reset(),a.while_init=!1}};a.$image.cropper(e),a.cropper=a.$image.data("cropper"),a.$image.on("CROPPERPATTERN.VISIBLE",function(){a.notify_visible()})}});return c}),define("/home/workspacejensens/bda.aaf.site/devsrc/plone.app.imagecropping/src/plone/app/imagecropping/browser/static/cropperpattern.js",function(){}),require(["pat-base","jquery"],function(a,b){"use strict";var c=a.extend({name:"imagecropsave",trigger:".pat-imagecrop-scaleselect",parser:"mockup",trigger_notify_visible:function(a){console.log("Trigger event");var c=b.Event("CROPPERPATTERN.VISIBLE");a.trigger(c)},toggle_fieldset:function(a){var c=b(a).data("forfieldset"),d=b(c);if(!d.hasClass("active")){b("fieldset.active",self.$el).removeClass("active").addClass("inactive"),b("nav a.active",self.$el).removeClass("active").addClass("inactive"),d.removeClass("inactive").addClass("active"),b(a).removeClass("inactive").addClass("active");var e=b("div.singlecroppingarea.active img.main-image",d);this.trigger_notify_visible(e)}},toggle_li:function(a){var c=b(a),d=b(c.parent());if(!c.hasClass("active")){b("li.list-group-item.active",d).removeClass("active").addClass("inactive"),c.removeClass("inactive").addClass("active");var e=b(b(c.data("cropping-area"))),f=b(e.parent()),g=b(".singlecroppingarea.active",f);g.removeClass("active").addClass("inactive"),e.removeClass("inactive").addClass("active");var h=b("img.main-image",e);this.trigger_notify_visible(h)}},set_preview_dimensions:function(a){var c=b(a),d=b(".preview-container",c),e=b(".crop-preview",d),f=parseFloat(d.data("target-width")),g=parseFloat(d.data("target-height")),h=c.width(),i=null;i=h>=f?g:g*h/f,d.width(h),d.height(i),e.width(h),e.height(i)},init:function(){var a=this;b("nav a",a.$el).each(function(c){var d=this;b(d).click(function(){a.toggle_fieldset(d)})}),b("fieldset",a.$el).each(function(c){var d=this;b("li.list-group-item.scalable",b(d)).each(function(c){var d=this;a.set_preview_dimensions(d),b(d).click(function(){a.toggle_li(d)})}),c>0&&setTimeout(function(){b(d).removeClass("active").addClass("inactive")},200)})}});return c}),define("/home/workspacejensens/bda.aaf.site/devsrc/plone.app.imagecropping/src/plone/app/imagecropping/browser/static/cropscaleselect.js",function(){});
//# sourceMappingURL=imagecropping-compiled.js.map