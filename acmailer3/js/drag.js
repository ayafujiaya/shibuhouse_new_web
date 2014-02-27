var nodrag = 1;

function SetNodrag(id) {
	nodrag = id;
}

function beginScript() {
    var rs = DragHandler.attach(document.getElementById('confirm'));
}
var DragHandler = {

    _oElem : null,
    attach : function(oElem) {
        oElem.onmousedown = DragHandler._dragBegin;
        return oElem;
    },
    _dragBegin : function(e) {
        var oElem = DragHandler._oElem = this;
        if (isNaN(parseInt(oElem.style.left))) { oElem.style.left = '0px'; }
        if (isNaN(parseInt(oElem.style.top))) { oElem.style.top = '0px'; }
        var x = parseInt(oElem.style.left);
        var y = parseInt(oElem.style.top);
        e = e ? e : window.event;
        oElem.mouseX = e.clientX;
        oElem.mouseY = e.clientY;
        document.onmousemove = DragHandler._drag;
        document.onmouseup = DragHandler._dragEnd;
        return false;
    },
    _drag : function(e) {
        var oElem = DragHandler._oElem;
        var x = parseInt(oElem.style.left);
        var y = parseInt(oElem.style.top);
        e = e ? e : window.event;

// // 
// // if (typeof document.activeElement == "undefined")
// // 	document.addEventListener("focus", function(event) {
// // 		document.activeElement = (event.target.nodeType == Node.TEXT_NODE) ? event.target.parentNode : event.target;
// // 	}, false);
// // 		
// 		
// 		// 
// // 		alert(document.activeElement.id + ":" + oElem.id);
// 		if (document.getElementById(oElem.id + '_bar')) {
// 			if (document.activeElement.id == oElem.id + '_bar') {
// 		        oElem.style.left = x + (e.clientX - oElem.mouseX) + 'px';
// 		        oElem.style.top = y + (e.clientY - oElem.mouseY) + 'px';
// 		        oElem.mouseX = e.clientX;
// 		        oElem.mouseY = e.clientY; 
// 			}
// 		} else {
// 			if (!nodrag) {
// 		        oElem.style.left = x + (e.clientX - oElem.mouseX) + 'px';
// 		        oElem.style.top = y + (e.clientY - oElem.mouseY) + 'px';
// 		        oElem.mouseX = e.clientX;
// 		        oElem.mouseY = e.clientY; 
// 			}
// 		}
		
		if (document.activeElement) {
			if (document.activeElement.id != "") {
				if (document.activeElement.id == oElem.id + '_bar') {
			        oElem.style.left = x + (e.clientX - oElem.mouseX) + 'px';
			        oElem.style.top = y + (e.clientY - oElem.mouseY) + 'px';
			        oElem.mouseX = e.clientX;
			        oElem.mouseY = e.clientY; 
				}
			} else {
				if (!nodrag) {
			        oElem.style.left = x + (e.clientX - oElem.mouseX) + 'px';
			        oElem.style.top = y + (e.clientY - oElem.mouseY) + 'px';
			        oElem.mouseX = e.clientX;
			        oElem.mouseY = e.clientY; 
				}
			}
		} else {
				if (!nodrag) {
			        oElem.style.left = x + (e.clientX - oElem.mouseX) + 'px';
			        oElem.style.top = y + (e.clientY - oElem.mouseY) + 'px';
			        oElem.mouseX = e.clientX;
			        oElem.mouseY = e.clientY; 
				}
		}
		
        return false;
    },
    _dragEnd : function() {
        var oElem = DragHandler._oElem;
        var x = parseInt(oElem.style.left);
        var y = parseInt(oElem.style.top);
        document.onmousemove = null;
        document.onmouseup = null;
        DragHandler._oElem = null;
    }
};
function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    } else {
        window.onload = function() {
            if (oldonload) {
                oldonload();
            }
            func();
        }
    }
}

addLoadEvent(function() {
beginScript();
});
