/*! jQuery UI - v1.10.2 - 2013-03-18
 * http://jqueryui.com
 * Includes: jquery.ui.core.js, jquery.ui.widget.js, jquery.ui.mouse.js, jquery.ui.position.js, jquery.ui.draggable.js, jquery.ui.resizable.js, jquery.ui.autocomplete.js, jquery.ui.button.js, jquery.ui.datepicker.js, jquery.ui.dialog.js, jquery.ui.menu.js, jquery.ui.progressbar.js, jquery.ui.spinner.js
 * Copyright 2013 jQuery Foundation and other contributors Licensed MIT */

(function (e, t) {
    function i(t, i) {
        var a, n, r, o = t.nodeName.toLowerCase();
        return"area" === o ? (a = t.parentNode, n = a.name, t.href && n && "map" === a.nodeName.toLowerCase() ? (r = e("img[usemap=#" + n + "]")[0], !!r && s(r)) : !1) : (/input|select|textarea|button|object/.test(o) ? !t.disabled : "a" === o ? t.href || i : i) && s(t)
    }

    function s(t) {
        return e.expr.filters.visible(t) && !e(t).parents().addBack().filter(function () {
            return"hidden" === e.css(this, "visibility")
        }).length
    }

    var a = 0, n = /^ui-id-\d+$/;
    e.ui = e.ui || {}, e.extend(e.ui, {version: "1.10.2", keyCode: {BACKSPACE: 8, COMMA: 188, DELETE: 46, DOWN: 40, END: 35, ENTER: 13, ESCAPE: 27, HOME: 36, LEFT: 37, NUMPAD_ADD: 107, NUMPAD_DECIMAL: 110, NUMPAD_DIVIDE: 111, NUMPAD_ENTER: 108, NUMPAD_MULTIPLY: 106, NUMPAD_SUBTRACT: 109, PAGE_DOWN: 34, PAGE_UP: 33, PERIOD: 190, RIGHT: 39, SPACE: 32, TAB: 9, UP: 38}}), e.fn.extend({focus: function (t) {
        return function (i, s) {
            return"number" == typeof i ? this.each(function () {
                var t = this;
                setTimeout(function () {
                    e(t).focus(), s && s.call(t)
                }, i)
            }) : t.apply(this, arguments)
        }
    }(e.fn.focus), scrollParent: function () {
        var t;
        return t = e.ui.ie && /(static|relative)/.test(this.css("position")) || /absolute/.test(this.css("position")) ? this.parents().filter(function () {
            return/(relative|absolute|fixed)/.test(e.css(this, "position")) && /(auto|scroll)/.test(e.css(this, "overflow") + e.css(this, "overflow-y") + e.css(this, "overflow-x"))
        }).eq(0) : this.parents().filter(function () {
            return/(auto|scroll)/.test(e.css(this, "overflow") + e.css(this, "overflow-y") + e.css(this, "overflow-x"))
        }).eq(0), /fixed/.test(this.css("position")) || !t.length ? e(document) : t
    }, zIndex: function (i) {
        if (i !== t)return this.css("zIndex", i);
        if (this.length)for (var s, a, n = e(this[0]); n.length && n[0] !== document;) {
            if (s = n.css("position"), ("absolute" === s || "relative" === s || "fixed" === s) && (a = parseInt(n.css("zIndex"), 10), !isNaN(a) && 0 !== a))return a;
            n = n.parent()
        }
        return 0
    }, uniqueId: function () {
        return this.each(function () {
            this.id || (this.id = "ui-id-" + ++a)
        })
    }, removeUniqueId: function () {
        return this.each(function () {
            n.test(this.id) && e(this).removeAttr("id")
        })
    }}), e.extend(e.expr[":"], {data: e.expr.createPseudo ? e.expr.createPseudo(function (t) {
        return function (i) {
            return!!e.data(i, t)
        }
    }) : function (t, i, s) {
        return!!e.data(t, s[3])
    }, focusable: function (t) {
        return i(t, !isNaN(e.attr(t, "tabindex")))
    }, tabbable: function (t) {
        var s = e.attr(t, "tabindex"), a = isNaN(s);
        return(a || s >= 0) && i(t, !a)
    }}), e("<a>").outerWidth(1).jquery || e.each(["Width", "Height"], function (i, s) {
        function a(t, i, s, a) {
            return e.each(n, function () {
                i -= parseFloat(e.css(t, "padding" + this)) || 0, s && (i -= parseFloat(e.css(t, "border" + this + "Width")) || 0), a && (i -= parseFloat(e.css(t, "margin" + this)) || 0)
            }), i
        }

        var n = "Width" === s ? ["Left", "Right"] : ["Top", "Bottom"], r = s.toLowerCase(), o = {innerWidth: e.fn.innerWidth, innerHeight: e.fn.innerHeight, outerWidth: e.fn.outerWidth, outerHeight: e.fn.outerHeight};
        e.fn["inner" + s] = function (i) {
            return i === t ? o["inner" + s].call(this) : this.each(function () {
                e(this).css(r, a(this, i) + "px")
            })
        }, e.fn["outer" + s] = function (t, i) {
            return"number" != typeof t ? o["outer" + s].call(this, t) : this.each(function () {
                e(this).css(r, a(this, t, !0, i) + "px")
            })
        }
    }), e.fn.addBack || (e.fn.addBack = function (e) {
        return this.add(null == e ? this.prevObject : this.prevObject.filter(e))
    }), e("<a>").data("a-b", "a").removeData("a-b").data("a-b") && (e.fn.removeData = function (t) {
        return function (i) {
            return arguments.length ? t.call(this, e.camelCase(i)) : t.call(this)
        }
    }(e.fn.removeData)), e.ui.ie = !!/msie [\w.]+/.exec(navigator.userAgent.toLowerCase()), e.support.selectstart = "onselectstart"in document.createElement("div"), e.fn.extend({disableSelection: function () {
        return this.bind((e.support.selectstart ? "selectstart" : "mousedown") + ".ui-disableSelection", function (e) {
            e.preventDefault()
        })
    }, enableSelection: function () {
        return this.unbind(".ui-disableSelection")
    }}), e.extend(e.ui, {plugin: {add: function (t, i, s) {
        var a, n = e.ui[t].prototype;
        for (a in s)n.plugins[a] = n.plugins[a] || [], n.plugins[a].push([i, s[a]])
    }, call: function (e, t, i) {
        var s, a = e.plugins[t];
        if (a && e.element[0].parentNode && 11 !== e.element[0].parentNode.nodeType)for (s = 0; a.length > s; s++)e.options[a[s][0]] && a[s][1].apply(e.element, i)
    }}, hasScroll: function (t, i) {
        if ("hidden" === e(t).css("overflow"))return!1;
        var s = i && "left" === i ? "scrollLeft" : "scrollTop", a = !1;
        return t[s] > 0 ? !0 : (t[s] = 1, a = t[s] > 0, t[s] = 0, a)
    }})
})(jQuery);
(function (e, t) {
    var i = 0, s = Array.prototype.slice, n = e.cleanData;
    e.cleanData = function (t) {
        for (var i, s = 0; null != (i = t[s]); s++)try {
            e(i).triggerHandler("remove")
        } catch (a) {
        }
        n(t)
    }, e.widget = function (i, s, n) {
        var a, r, o, h, l = {}, u = i.split(".")[0];
        i = i.split(".")[1], a = u + "-" + i, n || (n = s, s = e.Widget), e.expr[":"][a.toLowerCase()] = function (t) {
            return!!e.data(t, a)
        }, e[u] = e[u] || {}, r = e[u][i], o = e[u][i] = function (e, i) {
            return this._createWidget ? (arguments.length && this._createWidget(e, i), t) : new o(e, i)
        }, e.extend(o, r, {version: n.version, _proto: e.extend({}, n), _childConstructors: []}), h = new s, h.options = e.widget.extend({}, h.options), e.each(n, function (i, n) {
            return e.isFunction(n) ? (l[i] = function () {
                var e = function () {
                    return s.prototype[i].apply(this, arguments)
                }, t = function (e) {
                    return s.prototype[i].apply(this, e)
                };
                return function () {
                    var i, s = this._super, a = this._superApply;
                    return this._super = e, this._superApply = t, i = n.apply(this, arguments), this._super = s, this._superApply = a, i
                }
            }(), t) : (l[i] = n, t)
        }), o.prototype = e.widget.extend(h, {widgetEventPrefix: r ? h.widgetEventPrefix : i}, l, {constructor: o, namespace: u, widgetName: i, widgetFullName: a}), r ? (e.each(r._childConstructors, function (t, i) {
            var s = i.prototype;
            e.widget(s.namespace + "." + s.widgetName, o, i._proto)
        }), delete r._childConstructors) : s._childConstructors.push(o), e.widget.bridge(i, o)
    }, e.widget.extend = function (i) {
        for (var n, a, r = s.call(arguments, 1), o = 0, h = r.length; h > o; o++)for (n in r[o])a = r[o][n], r[o].hasOwnProperty(n) && a !== t && (i[n] = e.isPlainObject(a) ? e.isPlainObject(i[n]) ? e.widget.extend({}, i[n], a) : e.widget.extend({}, a) : a);
        return i
    }, e.widget.bridge = function (i, n) {
        var a = n.prototype.widgetFullName || i;
        e.fn[i] = function (r) {
            var o = "string" == typeof r, h = s.call(arguments, 1), l = this;
            return r = !o && h.length ? e.widget.extend.apply(null, [r].concat(h)) : r, o ? this.each(function () {
                var s, n = e.data(this, a);
                return n ? e.isFunction(n[r]) && "_" !== r.charAt(0) ? (s = n[r].apply(n, h), s !== n && s !== t ? (l = s && s.jquery ? l.pushStack(s.get()) : s, !1) : t) : e.error("no such method '" + r + "' for " + i + " widget instance") : e.error("cannot call methods on " + i + " prior to initialization; " + "attempted to call method '" + r + "'")
            }) : this.each(function () {
                var t = e.data(this, a);
                t ? t.option(r || {})._init() : e.data(this, a, new n(r, this))
            }), l
        }
    }, e.Widget = function () {
    }, e.Widget._childConstructors = [], e.Widget.prototype = {widgetName: "widget", widgetEventPrefix: "", defaultElement: "<div>", options: {disabled: !1, create: null}, _createWidget: function (t, s) {
        s = e(s || this.defaultElement || this)[0], this.element = e(s), this.uuid = i++, this.eventNamespace = "." + this.widgetName + this.uuid, this.options = e.widget.extend({}, this.options, this._getCreateOptions(), t), this.bindings = e(), this.hoverable = e(), this.focusable = e(), s !== this && (e.data(s, this.widgetFullName, this), this._on(!0, this.element, {remove: function (e) {
            e.target === s && this.destroy()
        }}), this.document = e(s.style ? s.ownerDocument : s.document || s), this.window = e(this.document[0].defaultView || this.document[0].parentWindow)), this._create(), this._trigger("create", null, this._getCreateEventData()), this._init()
    }, _getCreateOptions: e.noop, _getCreateEventData: e.noop, _create: e.noop, _init: e.noop, destroy: function () {
        this._destroy(), this.element.unbind(this.eventNamespace).removeData(this.widgetName).removeData(this.widgetFullName).removeData(e.camelCase(this.widgetFullName)), this.widget().unbind(this.eventNamespace).removeAttr("aria-disabled").removeClass(this.widgetFullName + "-disabled " + "ui-state-disabled"), this.bindings.unbind(this.eventNamespace), this.hoverable.removeClass("ui-state-hover"), this.focusable.removeClass("ui-state-focus")
    }, _destroy: e.noop, widget: function () {
        return this.element
    }, option: function (i, s) {
        var n, a, r, o = i;
        if (0 === arguments.length)return e.widget.extend({}, this.options);
        if ("string" == typeof i)if (o = {}, n = i.split("."), i = n.shift(), n.length) {
            for (a = o[i] = e.widget.extend({}, this.options[i]), r = 0; n.length - 1 > r; r++)a[n[r]] = a[n[r]] || {}, a = a[n[r]];
            if (i = n.pop(), s === t)return a[i] === t ? null : a[i];
            a[i] = s
        } else {
            if (s === t)return this.options[i] === t ? null : this.options[i];
            o[i] = s
        }
        return this._setOptions(o), this
    }, _setOptions: function (e) {
        var t;
        for (t in e)this._setOption(t, e[t]);
        return this
    }, _setOption: function (e, t) {
        return this.options[e] = t, "disabled" === e && (this.widget().toggleClass(this.widgetFullName + "-disabled ui-state-disabled", !!t).attr("aria-disabled", t), this.hoverable.removeClass("ui-state-hover"), this.focusable.removeClass("ui-state-focus")), this
    }, enable: function () {
        return this._setOption("disabled", !1)
    }, disable: function () {
        return this._setOption("disabled", !0)
    }, _on: function (i, s, n) {
        var a, r = this;
        "boolean" != typeof i && (n = s, s = i, i = !1), n ? (s = a = e(s), this.bindings = this.bindings.add(s)) : (n = s, s = this.element, a = this.widget()), e.each(n, function (n, o) {
            function h() {
                return i || r.options.disabled !== !0 && !e(this).hasClass("ui-state-disabled") ? ("string" == typeof o ? r[o] : o).apply(r, arguments) : t
            }

            "string" != typeof o && (h.guid = o.guid = o.guid || h.guid || e.guid++);
            var l = n.match(/^(\w+)\s*(.*)$/), u = l[1] + r.eventNamespace, c = l[2];
            c ? a.delegate(c, u, h) : s.bind(u, h)
        })
    }, _off: function (e, t) {
        t = (t || "").split(" ").join(this.eventNamespace + " ") + this.eventNamespace, e.unbind(t).undelegate(t)
    }, _delay: function (e, t) {
        function i() {
            return("string" == typeof e ? s[e] : e).apply(s, arguments)
        }

        var s = this;
        return setTimeout(i, t || 0)
    }, _hoverable: function (t) {
        this.hoverable = this.hoverable.add(t), this._on(t, {mouseenter: function (t) {
            e(t.currentTarget).addClass("ui-state-hover")
        }, mouseleave: function (t) {
            e(t.currentTarget).removeClass("ui-state-hover")
        }})
    }, _focusable: function (t) {
        this.focusable = this.focusable.add(t), this._on(t, {focusin: function (t) {
            e(t.currentTarget).addClass("ui-state-focus")
        }, focusout: function (t) {
            e(t.currentTarget).removeClass("ui-state-focus")
        }})
    }, _trigger: function (t, i, s) {
        var n, a, r = this.options[t];
        if (s = s || {}, i = e.Event(i), i.type = (t === this.widgetEventPrefix ? t : this.widgetEventPrefix + t).toLowerCase(), i.target = this.element[0], a = i.originalEvent)for (n in a)n in i || (i[n] = a[n]);
        return this.element.trigger(i, s), !(e.isFunction(r) && r.apply(this.element[0], [i].concat(s)) === !1 || i.isDefaultPrevented())
    }}, e.each({show: "fadeIn", hide: "fadeOut"}, function (t, i) {
        e.Widget.prototype["_" + t] = function (s, n, a) {
            "string" == typeof n && (n = {effect: n});
            var r, o = n ? n === !0 || "number" == typeof n ? i : n.effect || i : t;
            n = n || {}, "number" == typeof n && (n = {duration: n}), r = !e.isEmptyObject(n), n.complete = a, n.delay && s.delay(n.delay), r && e.effects && e.effects.effect[o] ? s[t](n) : o !== t && s[o] ? s[o](n.duration, n.easing, a) : s.queue(function (i) {
                e(this)[t](), a && a.call(s[0]), i()
            })
        }
    })
})(jQuery);
(function (e) {
    var t = !1;
    e(document).mouseup(function () {
        t = !1
    }), e.widget("ui.mouse", {version: "1.10.2", options: {cancel: "input,textarea,button,select,option", distance: 1, delay: 0}, _mouseInit: function () {
        var t = this;
        this.element.bind("mousedown." + this.widgetName,function (e) {
            return t._mouseDown(e)
        }).bind("click." + this.widgetName, function (i) {
                return!0 === e.data(i.target, t.widgetName + ".preventClickEvent") ? (e.removeData(i.target, t.widgetName + ".preventClickEvent"), i.stopImmediatePropagation(), !1) : undefined
            }), this.started = !1
    }, _mouseDestroy: function () {
        this.element.unbind("." + this.widgetName), this._mouseMoveDelegate && e(document).unbind("mousemove." + this.widgetName, this._mouseMoveDelegate).unbind("mouseup." + this.widgetName, this._mouseUpDelegate)
    }, _mouseDown: function (i) {
        if (!t) {
            this._mouseStarted && this._mouseUp(i), this._mouseDownEvent = i;
            var s = this, n = 1 === i.which, a = "string" == typeof this.options.cancel && i.target.nodeName ? e(i.target).closest(this.options.cancel).length : !1;
            return n && !a && this._mouseCapture(i) ? (this.mouseDelayMet = !this.options.delay, this.mouseDelayMet || (this._mouseDelayTimer = setTimeout(function () {
                s.mouseDelayMet = !0
            }, this.options.delay)), this._mouseDistanceMet(i) && this._mouseDelayMet(i) && (this._mouseStarted = this._mouseStart(i) !== !1, !this._mouseStarted) ? (i.preventDefault(), !0) : (!0 === e.data(i.target, this.widgetName + ".preventClickEvent") && e.removeData(i.target, this.widgetName + ".preventClickEvent"), this._mouseMoveDelegate = function (e) {
                return s._mouseMove(e)
            }, this._mouseUpDelegate = function (e) {
                return s._mouseUp(e)
            }, e(document).bind("mousemove." + this.widgetName, this._mouseMoveDelegate).bind("mouseup." + this.widgetName, this._mouseUpDelegate), i.preventDefault(), t = !0, !0)) : !0
        }
    }, _mouseMove: function (t) {
        return e.ui.ie && (!document.documentMode || 9 > document.documentMode) && !t.button ? this._mouseUp(t) : this._mouseStarted ? (this._mouseDrag(t), t.preventDefault()) : (this._mouseDistanceMet(t) && this._mouseDelayMet(t) && (this._mouseStarted = this._mouseStart(this._mouseDownEvent, t) !== !1, this._mouseStarted ? this._mouseDrag(t) : this._mouseUp(t)), !this._mouseStarted)
    }, _mouseUp: function (t) {
        return e(document).unbind("mousemove." + this.widgetName, this._mouseMoveDelegate).unbind("mouseup." + this.widgetName, this._mouseUpDelegate), this._mouseStarted && (this._mouseStarted = !1, t.target === this._mouseDownEvent.target && e.data(t.target, this.widgetName + ".preventClickEvent", !0), this._mouseStop(t)), !1
    }, _mouseDistanceMet: function (e) {
        return Math.max(Math.abs(this._mouseDownEvent.pageX - e.pageX), Math.abs(this._mouseDownEvent.pageY - e.pageY)) >= this.options.distance
    }, _mouseDelayMet: function () {
        return this.mouseDelayMet
    }, _mouseStart: function () {
    }, _mouseDrag: function () {
    }, _mouseStop: function () {
    }, _mouseCapture: function () {
        return!0
    }})
})(jQuery);
(function (t, e) {
    function i(t, e, i) {
        return[parseFloat(t[0]) * (p.test(t[0]) ? e / 100 : 1), parseFloat(t[1]) * (p.test(t[1]) ? i / 100 : 1)]
    }

    function s(e, i) {
        return parseInt(t.css(e, i), 10) || 0
    }

    function n(e) {
        var i = e[0];
        return 9 === i.nodeType ? {width: e.width(), height: e.height(), offset: {top: 0, left: 0}} : t.isWindow(i) ? {width: e.width(), height: e.height(), offset: {top: e.scrollTop(), left: e.scrollLeft()}} : i.preventDefault ? {width: 0, height: 0, offset: {top: i.pageY, left: i.pageX}} : {width: e.outerWidth(), height: e.outerHeight(), offset: e.offset()}
    }

    t.ui = t.ui || {};
    var a, o = Math.max, r = Math.abs, h = Math.round, l = /left|center|right/, c = /top|center|bottom/, u = /[\+\-]\d+(\.[\d]+)?%?/, d = /^\w+/, p = /%$/, f = t.fn.position;
    t.position = {scrollbarWidth: function () {
        if (a !== e)return a;
        var i, s, n = t("<div style='display:block;width:50px;height:50px;overflow:hidden;'><div style='height:100px;width:auto;'></div></div>"), o = n.children()[0];
        return t("body").append(n), i = o.offsetWidth, n.css("overflow", "scroll"), s = o.offsetWidth, i === s && (s = n[0].clientWidth), n.remove(), a = i - s
    }, getScrollInfo: function (e) {
        var i = e.isWindow ? "" : e.element.css("overflow-x"), s = e.isWindow ? "" : e.element.css("overflow-y"), n = "scroll" === i || "auto" === i && e.width < e.element[0].scrollWidth, a = "scroll" === s || "auto" === s && e.height < e.element[0].scrollHeight;
        return{width: a ? t.position.scrollbarWidth() : 0, height: n ? t.position.scrollbarWidth() : 0}
    }, getWithinInfo: function (e) {
        var i = t(e || window), s = t.isWindow(i[0]);
        return{element: i, isWindow: s, offset: i.offset() || {left: 0, top: 0}, scrollLeft: i.scrollLeft(), scrollTop: i.scrollTop(), width: s ? i.width() : i.outerWidth(), height: s ? i.height() : i.outerHeight()}
    }}, t.fn.position = function (e) {
        if (!e || !e.of)return f.apply(this, arguments);
        e = t.extend({}, e);
        var a, p, m, g, v, _, b = t(e.of), y = t.position.getWithinInfo(e.within), w = t.position.getScrollInfo(y), x = (e.collision || "flip").split(" "), k = {};
        return _ = n(b), b[0].preventDefault && (e.at = "left top"), p = _.width, m = _.height, g = _.offset, v = t.extend({}, g), t.each(["my", "at"], function () {
            var t, i, s = (e[this] || "").split(" ");
            1 === s.length && (s = l.test(s[0]) ? s.concat(["center"]) : c.test(s[0]) ? ["center"].concat(s) : ["center", "center"]), s[0] = l.test(s[0]) ? s[0] : "center", s[1] = c.test(s[1]) ? s[1] : "center", t = u.exec(s[0]), i = u.exec(s[1]), k[this] = [t ? t[0] : 0, i ? i[0] : 0], e[this] = [d.exec(s[0])[0], d.exec(s[1])[0]]
        }), 1 === x.length && (x[1] = x[0]), "right" === e.at[0] ? v.left += p : "center" === e.at[0] && (v.left += p / 2), "bottom" === e.at[1] ? v.top += m : "center" === e.at[1] && (v.top += m / 2), a = i(k.at, p, m), v.left += a[0], v.top += a[1], this.each(function () {
            var n, l, c = t(this), u = c.outerWidth(), d = c.outerHeight(), f = s(this, "marginLeft"), _ = s(this, "marginTop"), D = u + f + s(this, "marginRight") + w.width, T = d + _ + s(this, "marginBottom") + w.height, C = t.extend({}, v), M = i(k.my, c.outerWidth(), c.outerHeight());
            "right" === e.my[0] ? C.left -= u : "center" === e.my[0] && (C.left -= u / 2), "bottom" === e.my[1] ? C.top -= d : "center" === e.my[1] && (C.top -= d / 2), C.left += M[0], C.top += M[1], t.support.offsetFractions || (C.left = h(C.left), C.top = h(C.top)), n = {marginLeft: f, marginTop: _}, t.each(["left", "top"], function (i, s) {
                t.ui.position[x[i]] && t.ui.position[x[i]][s](C, {targetWidth: p, targetHeight: m, elemWidth: u, elemHeight: d, collisionPosition: n, collisionWidth: D, collisionHeight: T, offset: [a[0] + M[0], a[1] + M[1]], my: e.my, at: e.at, within: y, elem: c})
            }), e.using && (l = function (t) {
                var i = g.left - C.left, s = i + p - u, n = g.top - C.top, a = n + m - d, h = {target: {element: b, left: g.left, top: g.top, width: p, height: m}, element: {element: c, left: C.left, top: C.top, width: u, height: d}, horizontal: 0 > s ? "left" : i > 0 ? "right" : "center", vertical: 0 > a ? "top" : n > 0 ? "bottom" : "middle"};
                u > p && p > r(i + s) && (h.horizontal = "center"), d > m && m > r(n + a) && (h.vertical = "middle"), h.important = o(r(i), r(s)) > o(r(n), r(a)) ? "horizontal" : "vertical", e.using.call(this, t, h)
            }), c.offset(t.extend(C, {using: l}))
        })
    }, t.ui.position = {fit: {left: function (t, e) {
        var i, s = e.within, n = s.isWindow ? s.scrollLeft : s.offset.left, a = s.width, r = t.left - e.collisionPosition.marginLeft, h = n - r, l = r + e.collisionWidth - a - n;
        e.collisionWidth > a ? h > 0 && 0 >= l ? (i = t.left + h + e.collisionWidth - a - n, t.left += h - i) : t.left = l > 0 && 0 >= h ? n : h > l ? n + a - e.collisionWidth : n : h > 0 ? t.left += h : l > 0 ? t.left -= l : t.left = o(t.left - r, t.left)
    }, top: function (t, e) {
        var i, s = e.within, n = s.isWindow ? s.scrollTop : s.offset.top, a = e.within.height, r = t.top - e.collisionPosition.marginTop, h = n - r, l = r + e.collisionHeight - a - n;
        e.collisionHeight > a ? h > 0 && 0 >= l ? (i = t.top + h + e.collisionHeight - a - n, t.top += h - i) : t.top = l > 0 && 0 >= h ? n : h > l ? n + a - e.collisionHeight : n : h > 0 ? t.top += h : l > 0 ? t.top -= l : t.top = o(t.top - r, t.top)
    }}, flip: {left: function (t, e) {
        var i, s, n = e.within, a = n.offset.left + n.scrollLeft, o = n.width, h = n.isWindow ? n.scrollLeft : n.offset.left, l = t.left - e.collisionPosition.marginLeft, c = l - h, u = l + e.collisionWidth - o - h, d = "left" === e.my[0] ? -e.elemWidth : "right" === e.my[0] ? e.elemWidth : 0, p = "left" === e.at[0] ? e.targetWidth : "right" === e.at[0] ? -e.targetWidth : 0, f = -2 * e.offset[0];
        0 > c ? (i = t.left + d + p + f + e.collisionWidth - o - a, (0 > i || r(c) > i) && (t.left += d + p + f)) : u > 0 && (s = t.left - e.collisionPosition.marginLeft + d + p + f - h, (s > 0 || u > r(s)) && (t.left += d + p + f))
    }, top: function (t, e) {
        var i, s, n = e.within, a = n.offset.top + n.scrollTop, o = n.height, h = n.isWindow ? n.scrollTop : n.offset.top, l = t.top - e.collisionPosition.marginTop, c = l - h, u = l + e.collisionHeight - o - h, d = "top" === e.my[1], p = d ? -e.elemHeight : "bottom" === e.my[1] ? e.elemHeight : 0, f = "top" === e.at[1] ? e.targetHeight : "bottom" === e.at[1] ? -e.targetHeight : 0, m = -2 * e.offset[1];
        0 > c ? (s = t.top + p + f + m + e.collisionHeight - o - a, t.top + p + f + m > c && (0 > s || r(c) > s) && (t.top += p + f + m)) : u > 0 && (i = t.top - e.collisionPosition.marginTop + p + f + m - h, t.top + p + f + m > u && (i > 0 || u > r(i)) && (t.top += p + f + m))
    }}, flipfit: {left: function () {
        t.ui.position.flip.left.apply(this, arguments), t.ui.position.fit.left.apply(this, arguments)
    }, top: function () {
        t.ui.position.flip.top.apply(this, arguments), t.ui.position.fit.top.apply(this, arguments)
    }}}, function () {
        var e, i, s, n, a, o = document.getElementsByTagName("body")[0], r = document.createElement("div");
        e = document.createElement(o ? "div" : "body"), s = {visibility: "hidden", width: 0, height: 0, border: 0, margin: 0, background: "none"}, o && t.extend(s, {position: "absolute", left: "-1000px", top: "-1000px"});
        for (a in s)e.style[a] = s[a];
        e.appendChild(r), i = o || document.documentElement, i.insertBefore(e, i.firstChild), r.style.cssText = "position: absolute; left: 10.7432222px;", n = t(r).offset().left, t.support.offsetFractions = n > 10 && 11 > n, e.innerHTML = "", i.removeChild(e)
    }()
})(jQuery);
(function (e) {
    e.widget("ui.draggable", e.ui.mouse, {version: "1.10.2", widgetEventPrefix: "drag", options: {addClasses: !0, appendTo: "parent", axis: !1, connectToSortable: !1, containment: !1, cursor: "auto", cursorAt: !1, grid: !1, handle: !1, helper: "original", iframeFix: !1, opacity: !1, refreshPositions: !1, revert: !1, revertDuration: 500, scope: "default", scroll: !0, scrollSensitivity: 20, scrollSpeed: 20, snap: !1, snapMode: "both", snapTolerance: 20, stack: !1, zIndex: !1, drag: null, start: null, stop: null}, _create: function () {
        "original" !== this.options.helper || /^(?:r|a|f)/.test(this.element.css("position")) || (this.element[0].style.position = "relative"), this.options.addClasses && this.element.addClass("ui-draggable"), this.options.disabled && this.element.addClass("ui-draggable-disabled"), this._mouseInit()
    }, _destroy: function () {
        this.element.removeClass("ui-draggable ui-draggable-dragging ui-draggable-disabled"), this._mouseDestroy()
    }, _mouseCapture: function (t) {
        var i = this.options;
        return this.helper || i.disabled || e(t.target).closest(".ui-resizable-handle").length > 0 ? !1 : (this.handle = this._getHandle(t), this.handle ? (e(i.iframeFix === !0 ? "iframe" : i.iframeFix).each(function () {
            e("<div class='ui-draggable-iframeFix' style='background: #fff;'></div>").css({width: this.offsetWidth + "px", height: this.offsetHeight + "px", position: "absolute", opacity: "0.001", zIndex: 1e3}).css(e(this).offset()).appendTo("body")
        }), !0) : !1)
    }, _mouseStart: function (t) {
        var i = this.options;
        return this.helper = this._createHelper(t), this.helper.addClass("ui-draggable-dragging"), this._cacheHelperProportions(), e.ui.ddmanager && (e.ui.ddmanager.current = this), this._cacheMargins(), this.cssPosition = this.helper.css("position"), this.scrollParent = this.helper.scrollParent(), this.offset = this.positionAbs = this.element.offset(), this.offset = {top: this.offset.top - this.margins.top, left: this.offset.left - this.margins.left}, e.extend(this.offset, {click: {left: t.pageX - this.offset.left, top: t.pageY - this.offset.top}, parent: this._getParentOffset(), relative: this._getRelativeOffset()}), this.originalPosition = this.position = this._generatePosition(t), this.originalPageX = t.pageX, this.originalPageY = t.pageY, i.cursorAt && this._adjustOffsetFromHelper(i.cursorAt), i.containment && this._setContainment(), this._trigger("start", t) === !1 ? (this._clear(), !1) : (this._cacheHelperProportions(), e.ui.ddmanager && !i.dropBehaviour && e.ui.ddmanager.prepareOffsets(this, t), this._mouseDrag(t, !0), e.ui.ddmanager && e.ui.ddmanager.dragStart(this, t), !0)
    }, _mouseDrag: function (t, i) {
        if (this.position = this._generatePosition(t), this.positionAbs = this._convertPositionTo("absolute"), !i) {
            var s = this._uiHash();
            if (this._trigger("drag", t, s) === !1)return this._mouseUp({}), !1;
            this.position = s.position
        }
        return this.options.axis && "y" === this.options.axis || (this.helper[0].style.left = this.position.left + "px"), this.options.axis && "x" === this.options.axis || (this.helper[0].style.top = this.position.top + "px"), e.ui.ddmanager && e.ui.ddmanager.drag(this, t), !1
    }, _mouseStop: function (t) {
        var i, s = this, n = !1, a = !1;
        for (e.ui.ddmanager && !this.options.dropBehaviour && (a = e.ui.ddmanager.drop(this, t)), this.dropped && (a = this.dropped, this.dropped = !1), i = this.element[0]; i && (i = i.parentNode);)i === document && (n = !0);
        return n || "original" !== this.options.helper ? ("invalid" === this.options.revert && !a || "valid" === this.options.revert && a || this.options.revert === !0 || e.isFunction(this.options.revert) && this.options.revert.call(this.element, a) ? e(this.helper).animate(this.originalPosition, parseInt(this.options.revertDuration, 10), function () {
            s._trigger("stop", t) !== !1 && s._clear()
        }) : this._trigger("stop", t) !== !1 && this._clear(), !1) : !1
    }, _mouseUp: function (t) {
        return e("div.ui-draggable-iframeFix").each(function () {
            this.parentNode.removeChild(this)
        }), e.ui.ddmanager && e.ui.ddmanager.dragStop(this, t), e.ui.mouse.prototype._mouseUp.call(this, t)
    }, cancel: function () {
        return this.helper.is(".ui-draggable-dragging") ? this._mouseUp({}) : this._clear(), this
    }, _getHandle: function (t) {
        return this.options.handle ? !!e(t.target).closest(this.element.find(this.options.handle)).length : !0
    }, _createHelper: function (t) {
        var i = this.options, s = e.isFunction(i.helper) ? e(i.helper.apply(this.element[0], [t])) : "clone" === i.helper ? this.element.clone().removeAttr("id") : this.element;
        return s.parents("body").length || s.appendTo("parent" === i.appendTo ? this.element[0].parentNode : i.appendTo), s[0] === this.element[0] || /(fixed|absolute)/.test(s.css("position")) || s.css("position", "absolute"), s
    }, _adjustOffsetFromHelper: function (t) {
        "string" == typeof t && (t = t.split(" ")), e.isArray(t) && (t = {left: +t[0], top: +t[1] || 0}), "left"in t && (this.offset.click.left = t.left + this.margins.left), "right"in t && (this.offset.click.left = this.helperProportions.width - t.right + this.margins.left), "top"in t && (this.offset.click.top = t.top + this.margins.top), "bottom"in t && (this.offset.click.top = this.helperProportions.height - t.bottom + this.margins.top)
    }, _getParentOffset: function () {
        this.offsetParent = this.helper.offsetParent();
        var t = this.offsetParent.offset();
        return"absolute" === this.cssPosition && this.scrollParent[0] !== document && e.contains(this.scrollParent[0], this.offsetParent[0]) && (t.left += this.scrollParent.scrollLeft(), t.top += this.scrollParent.scrollTop()), (this.offsetParent[0] === document.body || this.offsetParent[0].tagName && "html" === this.offsetParent[0].tagName.toLowerCase() && e.ui.ie) && (t = {top: 0, left: 0}), {top: t.top + (parseInt(this.offsetParent.css("borderTopWidth"), 10) || 0), left: t.left + (parseInt(this.offsetParent.css("borderLeftWidth"), 10) || 0)}
    }, _getRelativeOffset: function () {
        if ("relative" === this.cssPosition) {
            var e = this.element.position();
            return{top: e.top - (parseInt(this.helper.css("top"), 10) || 0) + this.scrollParent.scrollTop(), left: e.left - (parseInt(this.helper.css("left"), 10) || 0) + this.scrollParent.scrollLeft()}
        }
        return{top: 0, left: 0}
    }, _cacheMargins: function () {
        this.margins = {left: parseInt(this.element.css("marginLeft"), 10) || 0, top: parseInt(this.element.css("marginTop"), 10) || 0, right: parseInt(this.element.css("marginRight"), 10) || 0, bottom: parseInt(this.element.css("marginBottom"), 10) || 0}
    }, _cacheHelperProportions: function () {
        this.helperProportions = {width: this.helper.outerWidth(), height: this.helper.outerHeight()}
    }, _setContainment: function () {
        var t, i, s, n = this.options;
        if ("parent" === n.containment && (n.containment = this.helper[0].parentNode), ("document" === n.containment || "window" === n.containment) && (this.containment = ["document" === n.containment ? 0 : e(window).scrollLeft() - this.offset.relative.left - this.offset.parent.left, "document" === n.containment ? 0 : e(window).scrollTop() - this.offset.relative.top - this.offset.parent.top, ("document" === n.containment ? 0 : e(window).scrollLeft()) + e("document" === n.containment ? document : window).width() - this.helperProportions.width - this.margins.left, ("document" === n.containment ? 0 : e(window).scrollTop()) + (e("document" === n.containment ? document : window).height() || document.body.parentNode.scrollHeight) - this.helperProportions.height - this.margins.top]), /^(document|window|parent)$/.test(n.containment) || n.containment.constructor === Array)n.containment.constructor === Array && (this.containment = n.containment); else {
            if (i = e(n.containment), s = i[0], !s)return;
            t = "hidden" !== e(s).css("overflow"), this.containment = [(parseInt(e(s).css("borderLeftWidth"), 10) || 0) + (parseInt(e(s).css("paddingLeft"), 10) || 0), (parseInt(e(s).css("borderTopWidth"), 10) || 0) + (parseInt(e(s).css("paddingTop"), 10) || 0), (t ? Math.max(s.scrollWidth, s.offsetWidth) : s.offsetWidth) - (parseInt(e(s).css("borderRightWidth"), 10) || 0) - (parseInt(e(s).css("paddingRight"), 10) || 0) - this.helperProportions.width - this.margins.left - this.margins.right, (t ? Math.max(s.scrollHeight, s.offsetHeight) : s.offsetHeight) - (parseInt(e(s).css("borderBottomWidth"), 10) || 0) - (parseInt(e(s).css("paddingBottom"), 10) || 0) - this.helperProportions.height - this.margins.top - this.margins.bottom], this.relative_container = i
        }
    }, _convertPositionTo: function (t, i) {
        i || (i = this.position);
        var s = "absolute" === t ? 1 : -1, n = "absolute" !== this.cssPosition || this.scrollParent[0] !== document && e.contains(this.scrollParent[0], this.offsetParent[0]) ? this.scrollParent : this.offsetParent, a = /(html|body)/i.test(n[0].tagName);
        return{top: i.top + this.offset.relative.top * s + this.offset.parent.top * s - ("fixed" === this.cssPosition ? -this.scrollParent.scrollTop() : a ? 0 : n.scrollTop()) * s, left: i.left + this.offset.relative.left * s + this.offset.parent.left * s - ("fixed" === this.cssPosition ? -this.scrollParent.scrollLeft() : a ? 0 : n.scrollLeft()) * s}
    }, _generatePosition: function (t) {
        var i, s, n, a, o = this.options, r = "absolute" !== this.cssPosition || this.scrollParent[0] !== document && e.contains(this.scrollParent[0], this.offsetParent[0]) ? this.scrollParent : this.offsetParent, h = /(html|body)/i.test(r[0].tagName), l = t.pageX, u = t.pageY;
        return this.originalPosition && (this.containment && (this.relative_container ? (s = this.relative_container.offset(), i = [this.containment[0] + s.left, this.containment[1] + s.top, this.containment[2] + s.left, this.containment[3] + s.top]) : i = this.containment, t.pageX - this.offset.click.left < i[0] && (l = i[0] + this.offset.click.left), t.pageY - this.offset.click.top < i[1] && (u = i[1] + this.offset.click.top), t.pageX - this.offset.click.left > i[2] && (l = i[2] + this.offset.click.left), t.pageY - this.offset.click.top > i[3] && (u = i[3] + this.offset.click.top)), o.grid && (n = o.grid[1] ? this.originalPageY + Math.round((u - this.originalPageY) / o.grid[1]) * o.grid[1] : this.originalPageY, u = i ? n - this.offset.click.top >= i[1] || n - this.offset.click.top > i[3] ? n : n - this.offset.click.top >= i[1] ? n - o.grid[1] : n + o.grid[1] : n, a = o.grid[0] ? this.originalPageX + Math.round((l - this.originalPageX) / o.grid[0]) * o.grid[0] : this.originalPageX, l = i ? a - this.offset.click.left >= i[0] || a - this.offset.click.left > i[2] ? a : a - this.offset.click.left >= i[0] ? a - o.grid[0] : a + o.grid[0] : a)), {top: u - this.offset.click.top - this.offset.relative.top - this.offset.parent.top + ("fixed" === this.cssPosition ? -this.scrollParent.scrollTop() : h ? 0 : r.scrollTop()), left: l - this.offset.click.left - this.offset.relative.left - this.offset.parent.left + ("fixed" === this.cssPosition ? -this.scrollParent.scrollLeft() : h ? 0 : r.scrollLeft())}
    }, _clear: function () {
        this.helper.removeClass("ui-draggable-dragging"), this.helper[0] === this.element[0] || this.cancelHelperRemoval || this.helper.remove(), this.helper = null, this.cancelHelperRemoval = !1
    }, _trigger: function (t, i, s) {
        return s = s || this._uiHash(), e.ui.plugin.call(this, t, [i, s]), "drag" === t && (this.positionAbs = this._convertPositionTo("absolute")), e.Widget.prototype._trigger.call(this, t, i, s)
    }, plugins: {}, _uiHash: function () {
        return{helper: this.helper, position: this.position, originalPosition: this.originalPosition, offset: this.positionAbs}
    }}), e.ui.plugin.add("draggable", "connectToSortable", {start: function (t, i) {
        var s = e(this).data("ui-draggable"), n = s.options, a = e.extend({}, i, {item: s.element});
        s.sortables = [], e(n.connectToSortable).each(function () {
            var i = e.data(this, "ui-sortable");
            i && !i.options.disabled && (s.sortables.push({instance: i, shouldRevert: i.options.revert}), i.refreshPositions(), i._trigger("activate", t, a))
        })
    }, stop: function (t, i) {
        var s = e(this).data("ui-draggable"), n = e.extend({}, i, {item: s.element});
        e.each(s.sortables, function () {
            this.instance.isOver ? (this.instance.isOver = 0, s.cancelHelperRemoval = !0, this.instance.cancelHelperRemoval = !1, this.shouldRevert && (this.instance.options.revert = this.shouldRevert), this.instance._mouseStop(t), this.instance.options.helper = this.instance.options._helper, "original" === s.options.helper && this.instance.currentItem.css({top: "auto", left: "auto"})) : (this.instance.cancelHelperRemoval = !1, this.instance._trigger("deactivate", t, n))
        })
    }, drag: function (t, i) {
        var s = e(this).data("ui-draggable"), n = this;
        e.each(s.sortables, function () {
            var a = !1, o = this;
            this.instance.positionAbs = s.positionAbs, this.instance.helperProportions = s.helperProportions, this.instance.offset.click = s.offset.click, this.instance._intersectsWith(this.instance.containerCache) && (a = !0, e.each(s.sortables, function () {
                return this.instance.positionAbs = s.positionAbs, this.instance.helperProportions = s.helperProportions, this.instance.offset.click = s.offset.click, this !== o && this.instance._intersectsWith(this.instance.containerCache) && e.contains(o.instance.element[0], this.instance.element[0]) && (a = !1), a
            })), a ? (this.instance.isOver || (this.instance.isOver = 1, this.instance.currentItem = e(n).clone().removeAttr("id").appendTo(this.instance.element).data("ui-sortable-item", !0), this.instance.options._helper = this.instance.options.helper, this.instance.options.helper = function () {
                return i.helper[0]
            }, t.target = this.instance.currentItem[0], this.instance._mouseCapture(t, !0), this.instance._mouseStart(t, !0, !0), this.instance.offset.click.top = s.offset.click.top, this.instance.offset.click.left = s.offset.click.left, this.instance.offset.parent.left -= s.offset.parent.left - this.instance.offset.parent.left, this.instance.offset.parent.top -= s.offset.parent.top - this.instance.offset.parent.top, s._trigger("toSortable", t), s.dropped = this.instance.element, s.currentItem = s.element, this.instance.fromOutside = s), this.instance.currentItem && this.instance._mouseDrag(t)) : this.instance.isOver && (this.instance.isOver = 0, this.instance.cancelHelperRemoval = !0, this.instance.options.revert = !1, this.instance._trigger("out", t, this.instance._uiHash(this.instance)), this.instance._mouseStop(t, !0), this.instance.options.helper = this.instance.options._helper, this.instance.currentItem.remove(), this.instance.placeholder && this.instance.placeholder.remove(), s._trigger("fromSortable", t), s.dropped = !1)
        })
    }}), e.ui.plugin.add("draggable", "cursor", {start: function () {
        var t = e("body"), i = e(this).data("ui-draggable").options;
        t.css("cursor") && (i._cursor = t.css("cursor")), t.css("cursor", i.cursor)
    }, stop: function () {
        var t = e(this).data("ui-draggable").options;
        t._cursor && e("body").css("cursor", t._cursor)
    }}), e.ui.plugin.add("draggable", "opacity", {start: function (t, i) {
        var s = e(i.helper), n = e(this).data("ui-draggable").options;
        s.css("opacity") && (n._opacity = s.css("opacity")), s.css("opacity", n.opacity)
    }, stop: function (t, i) {
        var s = e(this).data("ui-draggable").options;
        s._opacity && e(i.helper).css("opacity", s._opacity)
    }}), e.ui.plugin.add("draggable", "scroll", {start: function () {
        var t = e(this).data("ui-draggable");
        t.scrollParent[0] !== document && "HTML" !== t.scrollParent[0].tagName && (t.overflowOffset = t.scrollParent.offset())
    }, drag: function (t) {
        var i = e(this).data("ui-draggable"), s = i.options, n = !1;
        i.scrollParent[0] !== document && "HTML" !== i.scrollParent[0].tagName ? (s.axis && "x" === s.axis || (i.overflowOffset.top + i.scrollParent[0].offsetHeight - t.pageY < s.scrollSensitivity ? i.scrollParent[0].scrollTop = n = i.scrollParent[0].scrollTop + s.scrollSpeed : t.pageY - i.overflowOffset.top < s.scrollSensitivity && (i.scrollParent[0].scrollTop = n = i.scrollParent[0].scrollTop - s.scrollSpeed)), s.axis && "y" === s.axis || (i.overflowOffset.left + i.scrollParent[0].offsetWidth - t.pageX < s.scrollSensitivity ? i.scrollParent[0].scrollLeft = n = i.scrollParent[0].scrollLeft + s.scrollSpeed : t.pageX - i.overflowOffset.left < s.scrollSensitivity && (i.scrollParent[0].scrollLeft = n = i.scrollParent[0].scrollLeft - s.scrollSpeed))) : (s.axis && "x" === s.axis || (t.pageY - e(document).scrollTop() < s.scrollSensitivity ? n = e(document).scrollTop(e(document).scrollTop() - s.scrollSpeed) : e(window).height() - (t.pageY - e(document).scrollTop()) < s.scrollSensitivity && (n = e(document).scrollTop(e(document).scrollTop() + s.scrollSpeed))), s.axis && "y" === s.axis || (t.pageX - e(document).scrollLeft() < s.scrollSensitivity ? n = e(document).scrollLeft(e(document).scrollLeft() - s.scrollSpeed) : e(window).width() - (t.pageX - e(document).scrollLeft()) < s.scrollSensitivity && (n = e(document).scrollLeft(e(document).scrollLeft() + s.scrollSpeed)))), n !== !1 && e.ui.ddmanager && !s.dropBehaviour && e.ui.ddmanager.prepareOffsets(i, t)
    }}), e.ui.plugin.add("draggable", "snap", {start: function () {
        var t = e(this).data("ui-draggable"), i = t.options;
        t.snapElements = [], e(i.snap.constructor !== String ? i.snap.items || ":data(ui-draggable)" : i.snap).each(function () {
            var i = e(this), s = i.offset();
            this !== t.element[0] && t.snapElements.push({item: this, width: i.outerWidth(), height: i.outerHeight(), top: s.top, left: s.left})
        })
    }, drag: function (t, i) {
        var s, n, a, o, r, h, l, u, c, d, p = e(this).data("ui-draggable"), f = p.options, m = f.snapTolerance, g = i.offset.left, v = g + p.helperProportions.width, y = i.offset.top, b = y + p.helperProportions.height;
        for (c = p.snapElements.length - 1; c >= 0; c--)r = p.snapElements[c].left, h = r + p.snapElements[c].width, l = p.snapElements[c].top, u = l + p.snapElements[c].height, g > r - m && h + m > g && y > l - m && u + m > y || g > r - m && h + m > g && b > l - m && u + m > b || v > r - m && h + m > v && y > l - m && u + m > y || v > r - m && h + m > v && b > l - m && u + m > b ? ("inner" !== f.snapMode && (s = m >= Math.abs(l - b), n = m >= Math.abs(u - y), a = m >= Math.abs(r - v), o = m >= Math.abs(h - g), s && (i.position.top = p._convertPositionTo("relative", {top: l - p.helperProportions.height, left: 0}).top - p.margins.top), n && (i.position.top = p._convertPositionTo("relative", {top: u, left: 0}).top - p.margins.top), a && (i.position.left = p._convertPositionTo("relative", {top: 0, left: r - p.helperProportions.width}).left - p.margins.left), o && (i.position.left = p._convertPositionTo("relative", {top: 0, left: h}).left - p.margins.left)), d = s || n || a || o, "outer" !== f.snapMode && (s = m >= Math.abs(l - y), n = m >= Math.abs(u - b), a = m >= Math.abs(r - g), o = m >= Math.abs(h - v), s && (i.position.top = p._convertPositionTo("relative", {top: l, left: 0}).top - p.margins.top), n && (i.position.top = p._convertPositionTo("relative", {top: u - p.helperProportions.height, left: 0}).top - p.margins.top), a && (i.position.left = p._convertPositionTo("relative", {top: 0, left: r}).left - p.margins.left), o && (i.position.left = p._convertPositionTo("relative", {top: 0, left: h - p.helperProportions.width}).left - p.margins.left)), !p.snapElements[c].snapping && (s || n || a || o || d) && p.options.snap.snap && p.options.snap.snap.call(p.element, t, e.extend(p._uiHash(), {snapItem: p.snapElements[c].item})), p.snapElements[c].snapping = s || n || a || o || d) : (p.snapElements[c].snapping && p.options.snap.release && p.options.snap.release.call(p.element, t, e.extend(p._uiHash(), {snapItem: p.snapElements[c].item})), p.snapElements[c].snapping = !1)
    }}), e.ui.plugin.add("draggable", "stack", {start: function () {
        var t, i = this.data("ui-draggable").options, s = e.makeArray(e(i.stack)).sort(function (t, i) {
            return(parseInt(e(t).css("zIndex"), 10) || 0) - (parseInt(e(i).css("zIndex"), 10) || 0)
        });
        s.length && (t = parseInt(e(s[0]).css("zIndex"), 10) || 0, e(s).each(function (i) {
            e(this).css("zIndex", t + i)
        }), this.css("zIndex", t + s.length))
    }}), e.ui.plugin.add("draggable", "zIndex", {start: function (t, i) {
        var s = e(i.helper), n = e(this).data("ui-draggable").options;
        s.css("zIndex") && (n._zIndex = s.css("zIndex")), s.css("zIndex", n.zIndex)
    }, stop: function (t, i) {
        var s = e(this).data("ui-draggable").options;
        s._zIndex && e(i.helper).css("zIndex", s._zIndex)
    }})
})(jQuery);
(function (e) {
    function t(e) {
        return parseInt(e, 10) || 0
    }

    function i(e) {
        return!isNaN(parseInt(e, 10))
    }

    e.widget("ui.resizable", e.ui.mouse, {version: "1.10.2", widgetEventPrefix: "resize", options: {alsoResize: !1, animate: !1, animateDuration: "slow", animateEasing: "swing", aspectRatio: !1, autoHide: !1, containment: !1, ghost: !1, grid: !1, handles: "e,s,se", helper: !1, maxHeight: null, maxWidth: null, minHeight: 10, minWidth: 10, zIndex: 90, resize: null, start: null, stop: null}, _create: function () {
        var t, i, s, n, a, o = this, r = this.options;
        if (this.element.addClass("ui-resizable"), e.extend(this, {_aspectRatio: !!r.aspectRatio, aspectRatio: r.aspectRatio, originalElement: this.element, _proportionallyResizeElements: [], _helper: r.helper || r.ghost || r.animate ? r.helper || "ui-resizable-helper" : null}), this.element[0].nodeName.match(/canvas|textarea|input|select|button|img/i) && (this.element.wrap(e("<div class='ui-wrapper' style='overflow: hidden;'></div>").css({position: this.element.css("position"), width: this.element.outerWidth(), height: this.element.outerHeight(), top: this.element.css("top"), left: this.element.css("left")})), this.element = this.element.parent().data("ui-resizable", this.element.data("ui-resizable")), this.elementIsWrapper = !0, this.element.css({marginLeft: this.originalElement.css("marginLeft"), marginTop: this.originalElement.css("marginTop"), marginRight: this.originalElement.css("marginRight"), marginBottom: this.originalElement.css("marginBottom")}), this.originalElement.css({marginLeft: 0, marginTop: 0, marginRight: 0, marginBottom: 0}), this.originalResizeStyle = this.originalElement.css("resize"), this.originalElement.css("resize", "none"), this._proportionallyResizeElements.push(this.originalElement.css({position: "static", zoom: 1, display: "block"})), this.originalElement.css({margin: this.originalElement.css("margin")}), this._proportionallyResize()), this.handles = r.handles || (e(".ui-resizable-handle", this.element).length ? {n: ".ui-resizable-n", e: ".ui-resizable-e", s: ".ui-resizable-s", w: ".ui-resizable-w", se: ".ui-resizable-se", sw: ".ui-resizable-sw", ne: ".ui-resizable-ne", nw: ".ui-resizable-nw"} : "e,s,se"), this.handles.constructor === String)for ("all" === this.handles && (this.handles = "n,e,s,w,se,sw,ne,nw"), t = this.handles.split(","), this.handles = {}, i = 0; t.length > i; i++)s = e.trim(t[i]), a = "ui-resizable-" + s, n = e("<div class='ui-resizable-handle " + a + "'></div>"), n.css({zIndex: r.zIndex}), "se" === s && n.addClass("ui-icon ui-icon-gripsmall-diagonal-se"), this.handles[s] = ".ui-resizable-" + s, this.element.append(n);
        this._renderAxis = function (t) {
            var i, s, n, a;
            t = t || this.element;
            for (i in this.handles)this.handles[i].constructor === String && (this.handles[i] = e(this.handles[i], this.element).show()), this.elementIsWrapper && this.originalElement[0].nodeName.match(/textarea|input|select|button/i) && (s = e(this.handles[i], this.element), a = /sw|ne|nw|se|n|s/.test(i) ? s.outerHeight() : s.outerWidth(), n = ["padding", /ne|nw|n/.test(i) ? "Top" : /se|sw|s/.test(i) ? "Bottom" : /^e$/.test(i) ? "Right" : "Left"].join(""), t.css(n, a), this._proportionallyResize()), e(this.handles[i]).length
        }, this._renderAxis(this.element), this._handles = e(".ui-resizable-handle", this.element).disableSelection(), this._handles.mouseover(function () {
            o.resizing || (this.className && (n = this.className.match(/ui-resizable-(se|sw|ne|nw|n|e|s|w)/i)), o.axis = n && n[1] ? n[1] : "se")
        }), r.autoHide && (this._handles.hide(), e(this.element).addClass("ui-resizable-autohide").mouseenter(function () {
            r.disabled || (e(this).removeClass("ui-resizable-autohide"), o._handles.show())
        }).mouseleave(function () {
                r.disabled || o.resizing || (e(this).addClass("ui-resizable-autohide"), o._handles.hide())
            })), this._mouseInit()
    }, _destroy: function () {
        this._mouseDestroy();
        var t, i = function (t) {
            e(t).removeClass("ui-resizable ui-resizable-disabled ui-resizable-resizing").removeData("resizable").removeData("ui-resizable").unbind(".resizable").find(".ui-resizable-handle").remove()
        };
        return this.elementIsWrapper && (i(this.element), t = this.element, this.originalElement.css({position: t.css("position"), width: t.outerWidth(), height: t.outerHeight(), top: t.css("top"), left: t.css("left")}).insertAfter(t), t.remove()), this.originalElement.css("resize", this.originalResizeStyle), i(this.originalElement), this
    }, _mouseCapture: function (t) {
        var i, s, n = !1;
        for (i in this.handles)s = e(this.handles[i])[0], (s === t.target || e.contains(s, t.target)) && (n = !0);
        return!this.options.disabled && n
    }, _mouseStart: function (i) {
        var s, n, a, o = this.options, r = this.element.position(), h = this.element;
        return this.resizing = !0, /absolute/.test(h.css("position")) ? h.css({position: "absolute", top: h.css("top"), left: h.css("left")}) : h.is(".ui-draggable") && h.css({position: "absolute", top: r.top, left: r.left}), this._renderProxy(), s = t(this.helper.css("left")), n = t(this.helper.css("top")), o.containment && (s += e(o.containment).scrollLeft() || 0, n += e(o.containment).scrollTop() || 0), this.offset = this.helper.offset(), this.position = {left: s, top: n}, this.size = this._helper ? {width: h.outerWidth(), height: h.outerHeight()} : {width: h.width(), height: h.height()}, this.originalSize = this._helper ? {width: h.outerWidth(), height: h.outerHeight()} : {width: h.width(), height: h.height()}, this.originalPosition = {left: s, top: n}, this.sizeDiff = {width: h.outerWidth() - h.width(), height: h.outerHeight() - h.height()}, this.originalMousePosition = {left: i.pageX, top: i.pageY}, this.aspectRatio = "number" == typeof o.aspectRatio ? o.aspectRatio : this.originalSize.width / this.originalSize.height || 1, a = e(".ui-resizable-" + this.axis).css("cursor"), e("body").css("cursor", "auto" === a ? this.axis + "-resize" : a), h.addClass("ui-resizable-resizing"), this._propagate("start", i), !0
    }, _mouseDrag: function (t) {
        var i, s = this.helper, n = {}, a = this.originalMousePosition, o = this.axis, r = this.position.top, h = this.position.left, l = this.size.width, u = this.size.height, c = t.pageX - a.left || 0, d = t.pageY - a.top || 0, p = this._change[o];
        return p ? (i = p.apply(this, [t, c, d]), this._updateVirtualBoundaries(t.shiftKey), (this._aspectRatio || t.shiftKey) && (i = this._updateRatio(i, t)), i = this._respectSize(i, t), this._updateCache(i), this._propagate("resize", t), this.position.top !== r && (n.top = this.position.top + "px"), this.position.left !== h && (n.left = this.position.left + "px"), this.size.width !== l && (n.width = this.size.width + "px"), this.size.height !== u && (n.height = this.size.height + "px"), s.css(n), !this._helper && this._proportionallyResizeElements.length && this._proportionallyResize(), e.isEmptyObject(n) || this._trigger("resize", t, this.ui()), !1) : !1
    }, _mouseStop: function (t) {
        this.resizing = !1;
        var i, s, n, a, o, r, h, l = this.options, u = this;
        return this._helper && (i = this._proportionallyResizeElements, s = i.length && /textarea/i.test(i[0].nodeName), n = s && e.ui.hasScroll(i[0], "left") ? 0 : u.sizeDiff.height, a = s ? 0 : u.sizeDiff.width, o = {width: u.helper.width() - a, height: u.helper.height() - n}, r = parseInt(u.element.css("left"), 10) + (u.position.left - u.originalPosition.left) || null, h = parseInt(u.element.css("top"), 10) + (u.position.top - u.originalPosition.top) || null, l.animate || this.element.css(e.extend(o, {top: h, left: r})), u.helper.height(u.size.height), u.helper.width(u.size.width), this._helper && !l.animate && this._proportionallyResize()), e("body").css("cursor", "auto"), this.element.removeClass("ui-resizable-resizing"), this._propagate("stop", t), this._helper && this.helper.remove(), !1
    }, _updateVirtualBoundaries: function (e) {
        var t, s, n, a, o, r = this.options;
        o = {minWidth: i(r.minWidth) ? r.minWidth : 0, maxWidth: i(r.maxWidth) ? r.maxWidth : 1 / 0, minHeight: i(r.minHeight) ? r.minHeight : 0, maxHeight: i(r.maxHeight) ? r.maxHeight : 1 / 0}, (this._aspectRatio || e) && (t = o.minHeight * this.aspectRatio, n = o.minWidth / this.aspectRatio, s = o.maxHeight * this.aspectRatio, a = o.maxWidth / this.aspectRatio, t > o.minWidth && (o.minWidth = t), n > o.minHeight && (o.minHeight = n), o.maxWidth > s && (o.maxWidth = s), o.maxHeight > a && (o.maxHeight = a)), this._vBoundaries = o
    }, _updateCache: function (e) {
        this.offset = this.helper.offset(), i(e.left) && (this.position.left = e.left), i(e.top) && (this.position.top = e.top), i(e.height) && (this.size.height = e.height), i(e.width) && (this.size.width = e.width)
    }, _updateRatio: function (e) {
        var t = this.position, s = this.size, n = this.axis;
        return i(e.height) ? e.width = e.height * this.aspectRatio : i(e.width) && (e.height = e.width / this.aspectRatio), "sw" === n && (e.left = t.left + (s.width - e.width), e.top = null), "nw" === n && (e.top = t.top + (s.height - e.height), e.left = t.left + (s.width - e.width)), e
    }, _respectSize: function (e) {
        var t = this._vBoundaries, s = this.axis, n = i(e.width) && t.maxWidth && t.maxWidth < e.width, a = i(e.height) && t.maxHeight && t.maxHeight < e.height, o = i(e.width) && t.minWidth && t.minWidth > e.width, r = i(e.height) && t.minHeight && t.minHeight > e.height, h = this.originalPosition.left + this.originalSize.width, l = this.position.top + this.size.height, u = /sw|nw|w/.test(s), c = /nw|ne|n/.test(s);
        return o && (e.width = t.minWidth), r && (e.height = t.minHeight), n && (e.width = t.maxWidth), a && (e.height = t.maxHeight), o && u && (e.left = h - t.minWidth), n && u && (e.left = h - t.maxWidth), r && c && (e.top = l - t.minHeight), a && c && (e.top = l - t.maxHeight), e.width || e.height || e.left || !e.top ? e.width || e.height || e.top || !e.left || (e.left = null) : e.top = null, e
    }, _proportionallyResize: function () {
        if (this._proportionallyResizeElements.length) {
            var e, t, i, s, n, a = this.helper || this.element;
            for (e = 0; this._proportionallyResizeElements.length > e; e++) {
                if (n = this._proportionallyResizeElements[e], !this.borderDif)for (this.borderDif = [], i = [n.css("borderTopWidth"), n.css("borderRightWidth"), n.css("borderBottomWidth"), n.css("borderLeftWidth")], s = [n.css("paddingTop"), n.css("paddingRight"), n.css("paddingBottom"), n.css("paddingLeft")], t = 0; i.length > t; t++)this.borderDif[t] = (parseInt(i[t], 10) || 0) + (parseInt(s[t], 10) || 0);
                n.css({height: a.height() - this.borderDif[0] - this.borderDif[2] || 0, width: a.width() - this.borderDif[1] - this.borderDif[3] || 0})
            }
        }
    }, _renderProxy: function () {
        var t = this.element, i = this.options;
        this.elementOffset = t.offset(), this._helper ? (this.helper = this.helper || e("<div style='overflow:hidden;'></div>"), this.helper.addClass(this._helper).css({width: this.element.outerWidth() - 1, height: this.element.outerHeight() - 1, position: "absolute", left: this.elementOffset.left + "px", top: this.elementOffset.top + "px", zIndex: ++i.zIndex}), this.helper.appendTo("body").disableSelection()) : this.helper = this.element
    }, _change: {e: function (e, t) {
        return{width: this.originalSize.width + t}
    }, w: function (e, t) {
        var i = this.originalSize, s = this.originalPosition;
        return{left: s.left + t, width: i.width - t}
    }, n: function (e, t, i) {
        var s = this.originalSize, n = this.originalPosition;
        return{top: n.top + i, height: s.height - i}
    }, s: function (e, t, i) {
        return{height: this.originalSize.height + i}
    }, se: function (t, i, s) {
        return e.extend(this._change.s.apply(this, arguments), this._change.e.apply(this, [t, i, s]))
    }, sw: function (t, i, s) {
        return e.extend(this._change.s.apply(this, arguments), this._change.w.apply(this, [t, i, s]))
    }, ne: function (t, i, s) {
        return e.extend(this._change.n.apply(this, arguments), this._change.e.apply(this, [t, i, s]))
    }, nw: function (t, i, s) {
        return e.extend(this._change.n.apply(this, arguments), this._change.w.apply(this, [t, i, s]))
    }}, _propagate: function (t, i) {
        e.ui.plugin.call(this, t, [i, this.ui()]), "resize" !== t && this._trigger(t, i, this.ui())
    }, plugins: {}, ui: function () {
        return{originalElement: this.originalElement, element: this.element, helper: this.helper, position: this.position, size: this.size, originalSize: this.originalSize, originalPosition: this.originalPosition}
    }}), e.ui.plugin.add("resizable", "animate", {stop: function (t) {
        var i = e(this).data("ui-resizable"), s = i.options, n = i._proportionallyResizeElements, a = n.length && /textarea/i.test(n[0].nodeName), o = a && e.ui.hasScroll(n[0], "left") ? 0 : i.sizeDiff.height, r = a ? 0 : i.sizeDiff.width, h = {width: i.size.width - r, height: i.size.height - o}, l = parseInt(i.element.css("left"), 10) + (i.position.left - i.originalPosition.left) || null, u = parseInt(i.element.css("top"), 10) + (i.position.top - i.originalPosition.top) || null;
        i.element.animate(e.extend(h, u && l ? {top: u, left: l} : {}), {duration: s.animateDuration, easing: s.animateEasing, step: function () {
            var s = {width: parseInt(i.element.css("width"), 10), height: parseInt(i.element.css("height"), 10), top: parseInt(i.element.css("top"), 10), left: parseInt(i.element.css("left"), 10)};
            n && n.length && e(n[0]).css({width: s.width, height: s.height}), i._updateCache(s), i._propagate("resize", t)
        }})
    }}), e.ui.plugin.add("resizable", "containment", {start: function () {
        var i, s, n, a, o, r, h, l = e(this).data("ui-resizable"), u = l.options, c = l.element, d = u.containment, p = d instanceof e ? d.get(0) : /parent/.test(d) ? c.parent().get(0) : d;
        p && (l.containerElement = e(p), /document/.test(d) || d === document ? (l.containerOffset = {left: 0, top: 0}, l.containerPosition = {left: 0, top: 0}, l.parentData = {element: e(document), left: 0, top: 0, width: e(document).width(), height: e(document).height() || document.body.parentNode.scrollHeight}) : (i = e(p), s = [], e(["Top", "Right", "Left", "Bottom"]).each(function (e, n) {
            s[e] = t(i.css("padding" + n))
        }), l.containerOffset = i.offset(), l.containerPosition = i.position(), l.containerSize = {height: i.innerHeight() - s[3], width: i.innerWidth() - s[1]}, n = l.containerOffset, a = l.containerSize.height, o = l.containerSize.width, r = e.ui.hasScroll(p, "left") ? p.scrollWidth : o, h = e.ui.hasScroll(p) ? p.scrollHeight : a, l.parentData = {element: p, left: n.left, top: n.top, width: r, height: h}))
    }, resize: function (t) {
        var i, s, n, a, o = e(this).data("ui-resizable"), r = o.options, h = o.containerOffset, l = o.position, u = o._aspectRatio || t.shiftKey, c = {top: 0, left: 0}, d = o.containerElement;
        d[0] !== document && /static/.test(d.css("position")) && (c = h), l.left < (o._helper ? h.left : 0) && (o.size.width = o.size.width + (o._helper ? o.position.left - h.left : o.position.left - c.left), u && (o.size.height = o.size.width / o.aspectRatio), o.position.left = r.helper ? h.left : 0), l.top < (o._helper ? h.top : 0) && (o.size.height = o.size.height + (o._helper ? o.position.top - h.top : o.position.top), u && (o.size.width = o.size.height * o.aspectRatio), o.position.top = o._helper ? h.top : 0), o.offset.left = o.parentData.left + o.position.left, o.offset.top = o.parentData.top + o.position.top, i = Math.abs((o._helper ? o.offset.left - c.left : o.offset.left - c.left) + o.sizeDiff.width), s = Math.abs((o._helper ? o.offset.top - c.top : o.offset.top - h.top) + o.sizeDiff.height), n = o.containerElement.get(0) === o.element.parent().get(0), a = /relative|absolute/.test(o.containerElement.css("position")), n && a && (i -= o.parentData.left), i + o.size.width >= o.parentData.width && (o.size.width = o.parentData.width - i, u && (o.size.height = o.size.width / o.aspectRatio)), s + o.size.height >= o.parentData.height && (o.size.height = o.parentData.height - s, u && (o.size.width = o.size.height * o.aspectRatio))
    }, stop: function () {
        var t = e(this).data("ui-resizable"), i = t.options, s = t.containerOffset, n = t.containerPosition, a = t.containerElement, o = e(t.helper), r = o.offset(), h = o.outerWidth() - t.sizeDiff.width, l = o.outerHeight() - t.sizeDiff.height;
        t._helper && !i.animate && /relative/.test(a.css("position")) && e(this).css({left: r.left - n.left - s.left, width: h, height: l}), t._helper && !i.animate && /static/.test(a.css("position")) && e(this).css({left: r.left - n.left - s.left, width: h, height: l})
    }}), e.ui.plugin.add("resizable", "alsoResize", {start: function () {
        var t = e(this).data("ui-resizable"), i = t.options, s = function (t) {
            e(t).each(function () {
                var t = e(this);
                t.data("ui-resizable-alsoresize", {width: parseInt(t.width(), 10), height: parseInt(t.height(), 10), left: parseInt(t.css("left"), 10), top: parseInt(t.css("top"), 10)})
            })
        };
        "object" != typeof i.alsoResize || i.alsoResize.parentNode ? s(i.alsoResize) : i.alsoResize.length ? (i.alsoResize = i.alsoResize[0], s(i.alsoResize)) : e.each(i.alsoResize, function (e) {
            s(e)
        })
    }, resize: function (t, i) {
        var s = e(this).data("ui-resizable"), n = s.options, a = s.originalSize, o = s.originalPosition, r = {height: s.size.height - a.height || 0, width: s.size.width - a.width || 0, top: s.position.top - o.top || 0, left: s.position.left - o.left || 0}, h = function (t, s) {
            e(t).each(function () {
                var t = e(this), n = e(this).data("ui-resizable-alsoresize"), a = {}, o = s && s.length ? s : t.parents(i.originalElement[0]).length ? ["width", "height"] : ["width", "height", "top", "left"];
                e.each(o, function (e, t) {
                    var i = (n[t] || 0) + (r[t] || 0);
                    i && i >= 0 && (a[t] = i || null)
                }), t.css(a)
            })
        };
        "object" != typeof n.alsoResize || n.alsoResize.nodeType ? h(n.alsoResize) : e.each(n.alsoResize, function (e, t) {
            h(e, t)
        })
    }, stop: function () {
        e(this).removeData("resizable-alsoresize")
    }}), e.ui.plugin.add("resizable", "ghost", {start: function () {
        var t = e(this).data("ui-resizable"), i = t.options, s = t.size;
        t.ghost = t.originalElement.clone(), t.ghost.css({opacity: .25, display: "block", position: "relative", height: s.height, width: s.width, margin: 0, left: 0, top: 0}).addClass("ui-resizable-ghost").addClass("string" == typeof i.ghost ? i.ghost : ""), t.ghost.appendTo(t.helper)
    }, resize: function () {
        var t = e(this).data("ui-resizable");
        t.ghost && t.ghost.css({position: "relative", height: t.size.height, width: t.size.width})
    }, stop: function () {
        var t = e(this).data("ui-resizable");
        t.ghost && t.helper && t.helper.get(0).removeChild(t.ghost.get(0))
    }}), e.ui.plugin.add("resizable", "grid", {resize: function () {
        var t = e(this).data("ui-resizable"), i = t.options, s = t.size, n = t.originalSize, a = t.originalPosition, o = t.axis, r = "number" == typeof i.grid ? [i.grid, i.grid] : i.grid, h = r[0] || 1, l = r[1] || 1, u = Math.round((s.width - n.width) / h) * h, c = Math.round((s.height - n.height) / l) * l, d = n.width + u, p = n.height + c, f = i.maxWidth && d > i.maxWidth, m = i.maxHeight && p > i.maxHeight, g = i.minWidth && i.minWidth > d, v = i.minHeight && i.minHeight > p;
        i.grid = r, g && (d += h), v && (p += l), f && (d -= h), m && (p -= l), /^(se|s|e)$/.test(o) ? (t.size.width = d, t.size.height = p) : /^(ne)$/.test(o) ? (t.size.width = d, t.size.height = p, t.position.top = a.top - c) : /^(sw)$/.test(o) ? (t.size.width = d, t.size.height = p, t.position.left = a.left - u) : (t.size.width = d, t.size.height = p, t.position.top = a.top - c, t.position.left = a.left - u)
    }})
})(jQuery);
(function (e) {
    var t = 0;
    e.widget("ui.autocomplete", {version: "1.10.2", defaultElement: "<input>", options: {appendTo: null, autoFocus: !1, delay: 300, minLength: 1, position: {my: "left top", at: "left bottom", collision: "none"}, source: null, change: null, close: null, focus: null, open: null, response: null, search: null, select: null}, pending: 0, _create: function () {
        var t, i, s, n = this.element[0].nodeName.toLowerCase(), a = "textarea" === n, o = "input" === n;
        this.isMultiLine = a ? !0 : o ? !1 : this.element.prop("isContentEditable"), this.valueMethod = this.element[a || o ? "val" : "text"], this.isNewMenu = !0, this.element.addClass("ui-autocomplete-input").attr("autocomplete", "off"), this._on(this.element, {keydown: function (n) {
            if (this.element.prop("readOnly"))return t = !0, s = !0, i = !0, undefined;
            t = !1, s = !1, i = !1;
            var a = e.ui.keyCode;
            switch (n.keyCode) {
                case a.PAGE_UP:
                    t = !0, this._move("previousPage", n);
                    break;
                case a.PAGE_DOWN:
                    t = !0, this._move("nextPage", n);
                    break;
                case a.UP:
                    t = !0, this._keyEvent("previous", n);
                    break;
                case a.DOWN:
                    t = !0, this._keyEvent("next", n);
                    break;
                case a.ENTER:
                case a.NUMPAD_ENTER:
                    this.menu.active && (t = !0, n.preventDefault(), this.menu.select(n));
                    break;
                case a.TAB:
                    this.menu.active && this.menu.select(n);
                    break;
                case a.ESCAPE:
                    this.menu.element.is(":visible") && (this._value(this.term), this.close(n), n.preventDefault());
                    break;
                default:
                    i = !0, this._searchTimeout(n)
            }
        }, keypress: function (s) {
            if (t)return t = !1, s.preventDefault(), undefined;
            if (!i) {
                var n = e.ui.keyCode;
                switch (s.keyCode) {
                    case n.PAGE_UP:
                        this._move("previousPage", s);
                        break;
                    case n.PAGE_DOWN:
                        this._move("nextPage", s);
                        break;
                    case n.UP:
                        this._keyEvent("previous", s);
                        break;
                    case n.DOWN:
                        this._keyEvent("next", s)
                }
            }
        }, input: function (e) {
            return s ? (s = !1, e.preventDefault(), undefined) : (this._searchTimeout(e), undefined)
        }, focus: function () {
            this.selectedItem = null, this.previous = this._value()
        }, blur: function (e) {
            return this.cancelBlur ? (delete this.cancelBlur, undefined) : (clearTimeout(this.searching), this.close(e), this._change(e), undefined)
        }}), this._initSource(), this.menu = e("<ul>").addClass("ui-autocomplete ui-front").appendTo(this._appendTo()).menu({input: e(), role: null}).hide().data("ui-menu"), this._on(this.menu.element, {mousedown: function (t) {
            t.preventDefault(), this.cancelBlur = !0, this._delay(function () {
                delete this.cancelBlur
            });
            var i = this.menu.element[0];
            e(t.target).closest(".ui-menu-item").length || this._delay(function () {
                var t = this;
                this.document.one("mousedown", function (s) {
                    s.target === t.element[0] || s.target === i || e.contains(i, s.target) || t.close()
                })
            })
        }, menufocus: function (t, i) {
            if (this.isNewMenu && (this.isNewMenu = !1, t.originalEvent && /^mouse/.test(t.originalEvent.type)))return this.menu.blur(), this.document.one("mousemove", function () {
                e(t.target).trigger(t.originalEvent)
            }), undefined;
            var s = i.item.data("ui-autocomplete-item");
            !1 !== this._trigger("focus", t, {item: s}) ? t.originalEvent && /^key/.test(t.originalEvent.type) && this._value(s.value) : this.liveRegion.text(s.value)
        }, menuselect: function (e, t) {
            var i = t.item.data("ui-autocomplete-item"), s = this.previous;
            this.element[0] !== this.document[0].activeElement && (this.element.focus(), this.previous = s, this._delay(function () {
                this.previous = s, this.selectedItem = i
            })), !1 !== this._trigger("select", e, {item: i}) && this._value(i.value), this.term = this._value(), this.close(e), this.selectedItem = i
        }}), this.liveRegion = e("<span>", {role: "status", "aria-live": "polite"}).addClass("ui-helper-hidden-accessible").insertAfter(this.element), this._on(this.window, {beforeunload: function () {
            this.element.removeAttr("autocomplete")
        }})
    }, _destroy: function () {
        clearTimeout(this.searching), this.element.removeClass("ui-autocomplete-input").removeAttr("autocomplete"), this.menu.element.remove(), this.liveRegion.remove()
    }, _setOption: function (e, t) {
        this._super(e, t), "source" === e && this._initSource(), "appendTo" === e && this.menu.element.appendTo(this._appendTo()), "disabled" === e && t && this.xhr && this.xhr.abort()
    }, _appendTo: function () {
        var t = this.options.appendTo;
        return t && (t = t.jquery || t.nodeType ? e(t) : this.document.find(t).eq(0)), t || (t = this.element.closest(".ui-front")), t.length || (t = this.document[0].body), t
    }, _initSource: function () {
        var t, i, s = this;
        e.isArray(this.options.source) ? (t = this.options.source, this.source = function (i, s) {
            s(e.ui.autocomplete.filter(t, i.term))
        }) : "string" == typeof this.options.source ? (i = this.options.source, this.source = function (t, n) {
            s.xhr && s.xhr.abort(), s.xhr = e.ajax({url: i, data: t, dataType: "json", success: function (e) {
                n(e)
            }, error: function () {
                n([])
            }})
        }) : this.source = this.options.source
    }, _searchTimeout: function (e) {
        clearTimeout(this.searching), this.searching = this._delay(function () {
            this.term !== this._value() && (this.selectedItem = null, this.search(null, e))
        }, this.options.delay)
    }, search: function (e, t) {
        return e = null != e ? e : this._value(), this.term = this._value(), e.length < this.options.minLength ? this.close(t) : this._trigger("search", t) !== !1 ? this._search(e) : undefined
    }, _search: function (e) {
        this.pending++, this.element.addClass("ui-autocomplete-loading"), this.cancelSearch = !1, this.source({term: e}, this._response())
    }, _response: function () {
        var e = this, i = ++t;
        return function (s) {
            i === t && e.__response(s), e.pending--, e.pending || e.element.removeClass("ui-autocomplete-loading")
        }
    }, __response: function (e) {
        e && (e = this._normalize(e)), this._trigger("response", null, {content: e}), !this.options.disabled && e && e.length && !this.cancelSearch ? (this._suggest(e), this._trigger("open")) : this._close()
    }, close: function (e) {
        this.cancelSearch = !0, this._close(e)
    }, _close: function (e) {
        this.menu.element.is(":visible") && (this.menu.element.hide(), this.menu.blur(), this.isNewMenu = !0, this._trigger("close", e))
    }, _change: function (e) {
        this.previous !== this._value() && this._trigger("change", e, {item: this.selectedItem})
    }, _normalize: function (t) {
        return t.length && t[0].label && t[0].value ? t : e.map(t, function (t) {
            return"string" == typeof t ? {label: t, value: t} : e.extend({label: t.label || t.value, value: t.value || t.label}, t)
        })
    }, _suggest: function (t) {
        var i = this.menu.element.empty();
        this._renderMenu(i, t), this.isNewMenu = !0, this.menu.refresh(), i.show(), this._resizeMenu(), i.position(e.extend({of: this.element}, this.options.position)), this.options.autoFocus && this.menu.next()
    }, _resizeMenu: function () {
        var e = this.menu.element;
        e.outerWidth(Math.max(e.width("").outerWidth() + 1, this.element.outerWidth()))
    }, _renderMenu: function (t, i) {
        var s = this;
        e.each(i, function (e, i) {
            s._renderItemData(t, i)
        })
    }, _renderItemData: function (e, t) {
        return this._renderItem(e, t).data("ui-autocomplete-item", t)
    }, _renderItem: function (t, i) {
        return e("<li>").append(e("<a>").text(i.label)).appendTo(t)
    }, _move: function (e, t) {
        return this.menu.element.is(":visible") ? this.menu.isFirstItem() && /^previous/.test(e) || this.menu.isLastItem() && /^next/.test(e) ? (this._value(this.term), this.menu.blur(), undefined) : (this.menu[e](t), undefined) : (this.search(null, t), undefined)
    }, widget: function () {
        return this.menu.element
    }, _value: function () {
        return this.valueMethod.apply(this.element, arguments)
    }, _keyEvent: function (e, t) {
        (!this.isMultiLine || this.menu.element.is(":visible")) && (this._move(e, t), t.preventDefault())
    }}), e.extend(e.ui.autocomplete, {escapeRegex: function (e) {
        return e.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&")
    }, filter: function (t, i) {
        var s = RegExp(e.ui.autocomplete.escapeRegex(i), "i");
        return e.grep(t, function (e) {
            return s.test(e.label || e.value || e)
        })
    }}), e.widget("ui.autocomplete", e.ui.autocomplete, {options: {messages: {noResults: "No search results.", results: function (e) {
        return e + (e > 1 ? " results are" : " result is") + " available, use up and down arrow keys to navigate."
    }}}, __response: function (e) {
        var t;
        this._superApply(arguments), this.options.disabled || this.cancelSearch || (t = e && e.length ? this.options.messages.results(e.length) : this.options.messages.noResults, this.liveRegion.text(t))
    }})
})(jQuery);
(function (t) {
    var e, i, s, n, a = "ui-button ui-widget ui-state-default ui-corner-all", o = "ui-state-hover ui-state-active ", r = "ui-button-icons-only ui-button-icon-only ui-button-text-icons ui-button-text-icon-primary ui-button-text-icon-secondary ui-button-text-only", h = function () {
        var e = t(this).find(":ui-button");
        setTimeout(function () {
            e.button("refresh")
        }, 1)
    }, l = function (e) {
        var i = e.name, s = e.form, n = t([]);
        return i && (i = i.replace(/'/g, "\\'"), n = s ? t(s).find("[name='" + i + "']") : t("[name='" + i + "']", e.ownerDocument).filter(function () {
            return!this.form
        })), n
    };
    t.widget("ui.button", {version: "1.10.2", defaultElement: "<button>", options: {disabled: null, text: !0, label: null, icons: {primary: null, secondary: null}}, _create: function () {
        this.element.closest("form").unbind("reset" + this.eventNamespace).bind("reset" + this.eventNamespace, h), "boolean" != typeof this.options.disabled ? this.options.disabled = !!this.element.prop("disabled") : this.element.prop("disabled", this.options.disabled), this._determineButtonType(), this.hasTitle = !!this.buttonElement.attr("title");
        var o = this, r = this.options, c = "checkbox" === this.type || "radio" === this.type, u = c ? "" : "ui-state-active", d = "ui-state-focus";
        null === r.label && (r.label = "input" === this.type ? this.buttonElement.val() : this.buttonElement.html()), this._hoverable(this.buttonElement), this.buttonElement.addClass(a).attr("role", "button").bind("mouseenter" + this.eventNamespace,function () {
            r.disabled || this === e && t(this).addClass("ui-state-active")
        }).bind("mouseleave" + this.eventNamespace,function () {
                r.disabled || t(this).removeClass(u)
            }).bind("click" + this.eventNamespace, function (t) {
                r.disabled && (t.preventDefault(), t.stopImmediatePropagation())
            }), this.element.bind("focus" + this.eventNamespace,function () {
            o.buttonElement.addClass(d)
        }).bind("blur" + this.eventNamespace, function () {
                o.buttonElement.removeClass(d)
            }), c && (this.element.bind("change" + this.eventNamespace, function () {
            n || o.refresh()
        }), this.buttonElement.bind("mousedown" + this.eventNamespace,function (t) {
            r.disabled || (n = !1, i = t.pageX, s = t.pageY)
        }).bind("mouseup" + this.eventNamespace, function (t) {
                r.disabled || (i !== t.pageX || s !== t.pageY) && (n = !0)
            })), "checkbox" === this.type ? this.buttonElement.bind("click" + this.eventNamespace, function () {
            return r.disabled || n ? !1 : undefined
        }) : "radio" === this.type ? this.buttonElement.bind("click" + this.eventNamespace, function () {
            if (r.disabled || n)return!1;
            t(this).addClass("ui-state-active"), o.buttonElement.attr("aria-pressed", "true");
            var e = o.element[0];
            l(e).not(e).map(function () {
                return t(this).button("widget")[0]
            }).removeClass("ui-state-active").attr("aria-pressed", "false")
        }) : (this.buttonElement.bind("mousedown" + this.eventNamespace,function () {
            return r.disabled ? !1 : (t(this).addClass("ui-state-active"), e = this, o.document.one("mouseup", function () {
                e = null
            }), undefined)
        }).bind("mouseup" + this.eventNamespace,function () {
                return r.disabled ? !1 : (t(this).removeClass("ui-state-active"), undefined)
            }).bind("keydown" + this.eventNamespace,function (e) {
                return r.disabled ? !1 : ((e.keyCode === t.ui.keyCode.SPACE || e.keyCode === t.ui.keyCode.ENTER) && t(this).addClass("ui-state-active"), undefined)
            }).bind("keyup" + this.eventNamespace + " blur" + this.eventNamespace, function () {
                t(this).removeClass("ui-state-active")
            }), this.buttonElement.is("a") && this.buttonElement.keyup(function (e) {
            e.keyCode === t.ui.keyCode.SPACE && t(this).click()
        })), this._setOption("disabled", r.disabled), this._resetButton()
    }, _determineButtonType: function () {
        var t, e, i;
        this.type = this.element.is("[type=checkbox]") ? "checkbox" : this.element.is("[type=radio]") ? "radio" : this.element.is("input") ? "input" : "button", "checkbox" === this.type || "radio" === this.type ? (t = this.element.parents().last(), e = "label[for='" + this.element.attr("id") + "']", this.buttonElement = t.find(e), this.buttonElement.length || (t = t.length ? t.siblings() : this.element.siblings(), this.buttonElement = t.filter(e), this.buttonElement.length || (this.buttonElement = t.find(e))), this.element.addClass("ui-helper-hidden-accessible"), i = this.element.is(":checked"), i && this.buttonElement.addClass("ui-state-active"), this.buttonElement.prop("aria-pressed", i)) : this.buttonElement = this.element
    }, widget: function () {
        return this.buttonElement
    }, _destroy: function () {
        this.element.removeClass("ui-helper-hidden-accessible"), this.buttonElement.removeClass(a + " " + o + " " + r).removeAttr("role").removeAttr("aria-pressed").html(this.buttonElement.find(".ui-button-text").html()), this.hasTitle || this.buttonElement.removeAttr("title")
    }, _setOption: function (t, e) {
        return this._super(t, e), "disabled" === t ? (e ? this.element.prop("disabled", !0) : this.element.prop("disabled", !1), undefined) : (this._resetButton(), undefined)
    }, refresh: function () {
        var e = this.element.is("input, button") ? this.element.is(":disabled") : this.element.hasClass("ui-button-disabled");
        e !== this.options.disabled && this._setOption("disabled", e), "radio" === this.type ? l(this.element[0]).each(function () {
            t(this).is(":checked") ? t(this).button("widget").addClass("ui-state-active").attr("aria-pressed", "true") : t(this).button("widget").removeClass("ui-state-active").attr("aria-pressed", "false")
        }) : "checkbox" === this.type && (this.element.is(":checked") ? this.buttonElement.addClass("ui-state-active").attr("aria-pressed", "true") : this.buttonElement.removeClass("ui-state-active").attr("aria-pressed", "false"))
    }, _resetButton: function () {
        if ("input" === this.type)return this.options.label && this.element.val(this.options.label), undefined;
        var e = this.buttonElement.removeClass(r), i = t("<span></span>", this.document[0]).addClass("ui-button-text").html(this.options.label).appendTo(e.empty()).text(), s = this.options.icons, n = s.primary && s.secondary, a = [];
        s.primary || s.secondary ? (this.options.text && a.push("ui-button-text-icon" + (n ? "s" : s.primary ? "-primary" : "-secondary")), s.primary && e.prepend("<span class='ui-button-icon-primary ui-icon " + s.primary + "'></span>"), s.secondary && e.append("<span class='ui-button-icon-secondary ui-icon " + s.secondary + "'></span>"), this.options.text || (a.push(n ? "ui-button-icons-only" : "ui-button-icon-only"), this.hasTitle || e.attr("title", t.trim(i)))) : a.push("ui-button-text-only"), e.addClass(a.join(" "))
    }}), t.widget("ui.buttonset", {version: "1.10.2", options: {items: "button, input[type=button], input[type=submit], input[type=reset], input[type=checkbox], input[type=radio], a, :data(ui-button)"}, _create: function () {
        this.element.addClass("ui-buttonset")
    }, _init: function () {
        this.refresh()
    }, _setOption: function (t, e) {
        "disabled" === t && this.buttons.button("option", t, e), this._super(t, e)
    }, refresh: function () {
        var e = "rtl" === this.element.css("direction");
        this.buttons = this.element.find(this.options.items).filter(":ui-button").button("refresh").end().not(":ui-button").button().end().map(function () {
            return t(this).button("widget")[0]
        }).removeClass("ui-corner-all ui-corner-left ui-corner-right").filter(":first").addClass(e ? "ui-corner-right" : "ui-corner-left").end().filter(":last").addClass(e ? "ui-corner-left" : "ui-corner-right").end().end()
    }, _destroy: function () {
        this.element.removeClass("ui-buttonset"), this.buttons.map(function () {
            return t(this).button("widget")[0]
        }).removeClass("ui-corner-left ui-corner-right").end().button("destroy")
    }})
})(jQuery);
(function (t, e) {
    function i() {
        this._curInst = null, this._keyEvent = !1, this._disabledInputs = [], this._datepickerShowing = !1, this._inDialog = !1, this._mainDivId = "ui-datepicker-div", this._inlineClass = "ui-datepicker-inline", this._appendClass = "ui-datepicker-append", this._triggerClass = "ui-datepicker-trigger", this._dialogClass = "ui-datepicker-dialog", this._disableClass = "ui-datepicker-disabled", this._unselectableClass = "ui-datepicker-unselectable", this._currentClass = "ui-datepicker-current-day", this._dayOverClass = "ui-datepicker-days-cell-over", this.regional = [], this.regional[""] = {closeText: "Done", prevText: "Prev", nextText: "Next", currentText: "Today", monthNames: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], monthNamesShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], dayNames: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], dayNamesShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"], dayNamesMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"], weekHeader: "Wk", dateFormat: "mm/dd/yy", firstDay: 0, isRTL: !1, showMonthAfterYear: !1, yearSuffix: ""}, this._defaults = {showOn: "focus", showAnim: "fadeIn", showOptions: {}, defaultDate: null, appendText: "", buttonText: "...", buttonImage: "", buttonImageOnly: !1, hideIfNoPrevNext: !1, navigationAsDateFormat: !1, gotoCurrent: !1, changeMonth: !1, changeYear: !1, yearRange: "c-10:c+10", showOtherMonths: !1, selectOtherMonths: !1, showWeek: !1, calculateWeek: this.iso8601Week, shortYearCutoff: "+10", minDate: null, maxDate: null, duration: "fast", beforeShowDay: null, beforeShow: null, onSelect: null, onChangeMonthYear: null, onClose: null, numberOfMonths: 1, showCurrentAtPos: 0, stepMonths: 1, stepBigMonths: 12, altField: "", altFormat: "", constrainInput: !0, showButtonPanel: !1, autoSize: !1, disabled: !1}, t.extend(this._defaults, this.regional[""]), this.dpDiv = s(t("<div id='" + this._mainDivId + "' class='ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all'></div>"))
    }

    function s(e) {
        var i = "button, .ui-datepicker-prev, .ui-datepicker-next, .ui-datepicker-calendar td a";
        return e.delegate(i, "mouseout",function () {
            t(this).removeClass("ui-state-hover"), -1 !== this.className.indexOf("ui-datepicker-prev") && t(this).removeClass("ui-datepicker-prev-hover"), -1 !== this.className.indexOf("ui-datepicker-next") && t(this).removeClass("ui-datepicker-next-hover")
        }).delegate(i, "mouseover", function () {
                t.datepicker._isDisabledDatepicker(a.inline ? e.parent()[0] : a.input[0]) || (t(this).parents(".ui-datepicker-calendar").find("a").removeClass("ui-state-hover"), t(this).addClass("ui-state-hover"), -1 !== this.className.indexOf("ui-datepicker-prev") && t(this).addClass("ui-datepicker-prev-hover"), -1 !== this.className.indexOf("ui-datepicker-next") && t(this).addClass("ui-datepicker-next-hover"))
            })
    }

    function n(e, i) {
        t.extend(e, i);
        for (var s in i)null == i[s] && (e[s] = i[s]);
        return e
    }

    t.extend(t.ui, {datepicker: {version: "1.10.2"}});
    var a, r = "datepicker", o = (new Date).getTime();
    t.extend(i.prototype, {markerClassName: "hasDatepicker", maxRows: 4, _widgetDatepicker: function () {
        return this.dpDiv
    }, setDefaults: function (t) {
        return n(this._defaults, t || {}), this
    }, _attachDatepicker: function (e, i) {
        var s, n, a;
        s = e.nodeName.toLowerCase(), n = "div" === s || "span" === s, e.id || (this.uuid += 1, e.id = "dp" + this.uuid), a = this._newInst(t(e), n), a.settings = t.extend({}, i || {}), "input" === s ? this._connectDatepicker(e, a) : n && this._inlineDatepicker(e, a)
    }, _newInst: function (e, i) {
        var n = e[0].id.replace(/([^A-Za-z0-9_\-])/g, "\\\\$1");
        return{id: n, input: e, selectedDay: 0, selectedMonth: 0, selectedYear: 0, drawMonth: 0, drawYear: 0, inline: i, dpDiv: i ? s(t("<div class='" + this._inlineClass + " ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all'></div>")) : this.dpDiv}
    }, _connectDatepicker: function (e, i) {
        var s = t(e);
        i.append = t([]), i.trigger = t([]), s.hasClass(this.markerClassName) || (this._attachments(s, i), s.addClass(this.markerClassName).keydown(this._doKeyDown).keypress(this._doKeyPress).keyup(this._doKeyUp), this._autoSize(i), t.data(e, r, i), i.settings.disabled && this._disableDatepicker(e))
    }, _attachments: function (e, i) {
        var s, n, a, r = this._get(i, "appendText"), o = this._get(i, "isRTL");
        i.append && i.append.remove(), r && (i.append = t("<span class='" + this._appendClass + "'>" + r + "</span>"), e[o ? "before" : "after"](i.append)), e.unbind("focus", this._showDatepicker), i.trigger && i.trigger.remove(), s = this._get(i, "showOn"), ("focus" === s || "both" === s) && e.focus(this._showDatepicker), ("button" === s || "both" === s) && (n = this._get(i, "buttonText"), a = this._get(i, "buttonImage"), i.trigger = t(this._get(i, "buttonImageOnly") ? t("<img/>").addClass(this._triggerClass).attr({src: a, alt: n, title: n}) : t("<button type='button'></button>").addClass(this._triggerClass).html(a ? t("<img/>").attr({src: a, alt: n, title: n}) : n)), e[o ? "before" : "after"](i.trigger), i.trigger.click(function () {
            return t.datepicker._datepickerShowing && t.datepicker._lastInput === e[0] ? t.datepicker._hideDatepicker() : t.datepicker._datepickerShowing && t.datepicker._lastInput !== e[0] ? (t.datepicker._hideDatepicker(), t.datepicker._showDatepicker(e[0])) : t.datepicker._showDatepicker(e[0]), !1
        }))
    }, _autoSize: function (t) {
        if (this._get(t, "autoSize") && !t.inline) {
            var e, i, s, n, a = new Date(2009, 11, 20), r = this._get(t, "dateFormat");
            r.match(/[DM]/) && (e = function (t) {
                for (i = 0, s = 0, n = 0; t.length > n; n++)t[n].length > i && (i = t[n].length, s = n);
                return s
            }, a.setMonth(e(this._get(t, r.match(/MM/) ? "monthNames" : "monthNamesShort"))), a.setDate(e(this._get(t, r.match(/DD/) ? "dayNames" : "dayNamesShort")) + 20 - a.getDay())), t.input.attr("size", this._formatDate(t, a).length)
        }
    }, _inlineDatepicker: function (e, i) {
        var s = t(e);
        s.hasClass(this.markerClassName) || (s.addClass(this.markerClassName).append(i.dpDiv), t.data(e, r, i), this._setDate(i, this._getDefaultDate(i), !0), this._updateDatepicker(i), this._updateAlternate(i), i.settings.disabled && this._disableDatepicker(e), i.dpDiv.css("display", "block"))
    }, _dialogDatepicker: function (e, i, s, a, o) {
        var h, l, c, u, d, p = this._dialogInst;
        return p || (this.uuid += 1, h = "dp" + this.uuid, this._dialogInput = t("<input type='text' id='" + h + "' style='position: absolute; top: -100px; width: 0px;'/>"), this._dialogInput.keydown(this._doKeyDown), t("body").append(this._dialogInput), p = this._dialogInst = this._newInst(this._dialogInput, !1), p.settings = {}, t.data(this._dialogInput[0], r, p)), n(p.settings, a || {}), i = i && i.constructor === Date ? this._formatDate(p, i) : i, this._dialogInput.val(i), this._pos = o ? o.length ? o : [o.pageX, o.pageY] : null, this._pos || (l = document.documentElement.clientWidth, c = document.documentElement.clientHeight, u = document.documentElement.scrollLeft || document.body.scrollLeft, d = document.documentElement.scrollTop || document.body.scrollTop, this._pos = [l / 2 - 100 + u, c / 2 - 150 + d]), this._dialogInput.css("left", this._pos[0] + 20 + "px").css("top", this._pos[1] + "px"), p.settings.onSelect = s, this._inDialog = !0, this.dpDiv.addClass(this._dialogClass), this._showDatepicker(this._dialogInput[0]), t.blockUI && t.blockUI(this.dpDiv), t.data(this._dialogInput[0], r, p), this
    }, _destroyDatepicker: function (e) {
        var i, s = t(e), n = t.data(e, r);
        s.hasClass(this.markerClassName) && (i = e.nodeName.toLowerCase(), t.removeData(e, r), "input" === i ? (n.append.remove(), n.trigger.remove(), s.removeClass(this.markerClassName).unbind("focus", this._showDatepicker).unbind("keydown", this._doKeyDown).unbind("keypress", this._doKeyPress).unbind("keyup", this._doKeyUp)) : ("div" === i || "span" === i) && s.removeClass(this.markerClassName).empty())
    }, _enableDatepicker: function (e) {
        var i, s, n = t(e), a = t.data(e, r);
        n.hasClass(this.markerClassName) && (i = e.nodeName.toLowerCase(), "input" === i ? (e.disabled = !1, a.trigger.filter("button").each(function () {
            this.disabled = !1
        }).end().filter("img").css({opacity: "1.0", cursor: ""})) : ("div" === i || "span" === i) && (s = n.children("." + this._inlineClass), s.children().removeClass("ui-state-disabled"), s.find("select.ui-datepicker-month, select.ui-datepicker-year").prop("disabled", !1)), this._disabledInputs = t.map(this._disabledInputs, function (t) {
            return t === e ? null : t
        }))
    }, _disableDatepicker: function (e) {
        var i, s, n = t(e), a = t.data(e, r);
        n.hasClass(this.markerClassName) && (i = e.nodeName.toLowerCase(), "input" === i ? (e.disabled = !0, a.trigger.filter("button").each(function () {
            this.disabled = !0
        }).end().filter("img").css({opacity: "0.5", cursor: "default"})) : ("div" === i || "span" === i) && (s = n.children("." + this._inlineClass), s.children().addClass("ui-state-disabled"), s.find("select.ui-datepicker-month, select.ui-datepicker-year").prop("disabled", !0)), this._disabledInputs = t.map(this._disabledInputs, function (t) {
            return t === e ? null : t
        }), this._disabledInputs[this._disabledInputs.length] = e)
    }, _isDisabledDatepicker: function (t) {
        if (!t)return!1;
        for (var e = 0; this._disabledInputs.length > e; e++)if (this._disabledInputs[e] === t)return!0;
        return!1
    }, _getInst: function (e) {
        try {
            return t.data(e, r)
        } catch (i) {
            throw"Missing instance data for this datepicker"
        }
    }, _optionDatepicker: function (i, s, a) {
        var r, o, h, l, c = this._getInst(i);
        return 2 === arguments.length && "string" == typeof s ? "defaults" === s ? t.extend({}, t.datepicker._defaults) : c ? "all" === s ? t.extend({}, c.settings) : this._get(c, s) : null : (r = s || {}, "string" == typeof s && (r = {}, r[s] = a), c && (this._curInst === c && this._hideDatepicker(), o = this._getDateDatepicker(i, !0), h = this._getMinMaxDate(c, "min"), l = this._getMinMaxDate(c, "max"), n(c.settings, r), null !== h && r.dateFormat !== e && r.minDate === e && (c.settings.minDate = this._formatDate(c, h)), null !== l && r.dateFormat !== e && r.maxDate === e && (c.settings.maxDate = this._formatDate(c, l)), "disabled"in r && (r.disabled ? this._disableDatepicker(i) : this._enableDatepicker(i)), this._attachments(t(i), c), this._autoSize(c), this._setDate(c, o), this._updateAlternate(c), this._updateDatepicker(c)), e)
    }, _changeDatepicker: function (t, e, i) {
        this._optionDatepicker(t, e, i)
    }, _refreshDatepicker: function (t) {
        var e = this._getInst(t);
        e && this._updateDatepicker(e)
    }, _setDateDatepicker: function (t, e) {
        var i = this._getInst(t);
        i && (this._setDate(i, e), this._updateDatepicker(i), this._updateAlternate(i))
    }, _getDateDatepicker: function (t, e) {
        var i = this._getInst(t);
        return i && !i.inline && this._setDateFromField(i, e), i ? this._getDate(i) : null
    }, _doKeyDown: function (e) {
        var i, s, n, a = t.datepicker._getInst(e.target), r = !0, o = a.dpDiv.is(".ui-datepicker-rtl");
        if (a._keyEvent = !0, t.datepicker._datepickerShowing)switch (e.keyCode) {
            case 9:
                t.datepicker._hideDatepicker(), r = !1;
                break;
            case 13:
                return n = t("td." + t.datepicker._dayOverClass + ":not(." + t.datepicker._currentClass + ")", a.dpDiv), n[0] && t.datepicker._selectDay(e.target, a.selectedMonth, a.selectedYear, n[0]), i = t.datepicker._get(a, "onSelect"), i ? (s = t.datepicker._formatDate(a), i.apply(a.input ? a.input[0] : null, [s, a])) : t.datepicker._hideDatepicker(), !1;
            case 27:
                t.datepicker._hideDatepicker();
                break;
            case 33:
                t.datepicker._adjustDate(e.target, e.ctrlKey ? -t.datepicker._get(a, "stepBigMonths") : -t.datepicker._get(a, "stepMonths"), "M");
                break;
            case 34:
                t.datepicker._adjustDate(e.target, e.ctrlKey ? +t.datepicker._get(a, "stepBigMonths") : +t.datepicker._get(a, "stepMonths"), "M");
                break;
            case 35:
                (e.ctrlKey || e.metaKey) && t.datepicker._clearDate(e.target), r = e.ctrlKey || e.metaKey;
                break;
            case 36:
                (e.ctrlKey || e.metaKey) && t.datepicker._gotoToday(e.target), r = e.ctrlKey || e.metaKey;
                break;
            case 37:
                (e.ctrlKey || e.metaKey) && t.datepicker._adjustDate(e.target, o ? 1 : -1, "D"), r = e.ctrlKey || e.metaKey, e.originalEvent.altKey && t.datepicker._adjustDate(e.target, e.ctrlKey ? -t.datepicker._get(a, "stepBigMonths") : -t.datepicker._get(a, "stepMonths"), "M");
                break;
            case 38:
                (e.ctrlKey || e.metaKey) && t.datepicker._adjustDate(e.target, -7, "D"), r = e.ctrlKey || e.metaKey;
                break;
            case 39:
                (e.ctrlKey || e.metaKey) && t.datepicker._adjustDate(e.target, o ? -1 : 1, "D"), r = e.ctrlKey || e.metaKey, e.originalEvent.altKey && t.datepicker._adjustDate(e.target, e.ctrlKey ? +t.datepicker._get(a, "stepBigMonths") : +t.datepicker._get(a, "stepMonths"), "M");
                break;
            case 40:
                (e.ctrlKey || e.metaKey) && t.datepicker._adjustDate(e.target, 7, "D"), r = e.ctrlKey || e.metaKey;
                break;
            default:
                r = !1
        } else 36 === e.keyCode && e.ctrlKey ? t.datepicker._showDatepicker(this) : r = !1;
        r && (e.preventDefault(), e.stopPropagation())
    }, _doKeyPress: function (i) {
        var s, n, a = t.datepicker._getInst(i.target);
        return t.datepicker._get(a, "constrainInput") ? (s = t.datepicker._possibleChars(t.datepicker._get(a, "dateFormat")), n = String.fromCharCode(null == i.charCode ? i.keyCode : i.charCode), i.ctrlKey || i.metaKey || " " > n || !s || s.indexOf(n) > -1) : e
    }, _doKeyUp: function (e) {
        var i, s = t.datepicker._getInst(e.target);
        if (s.input.val() !== s.lastVal)try {
            i = t.datepicker.parseDate(t.datepicker._get(s, "dateFormat"), s.input ? s.input.val() : null, t.datepicker._getFormatConfig(s)), i && (t.datepicker._setDateFromField(s), t.datepicker._updateAlternate(s), t.datepicker._updateDatepicker(s))
        } catch (n) {
        }
        return!0
    }, _showDatepicker: function (e) {
        if (e = e.target || e, "input" !== e.nodeName.toLowerCase() && (e = t("input", e.parentNode)[0]), !t.datepicker._isDisabledDatepicker(e) && t.datepicker._lastInput !== e) {
            var i, s, a, r, o, h, l;
            i = t.datepicker._getInst(e), t.datepicker._curInst && t.datepicker._curInst !== i && (t.datepicker._curInst.dpDiv.stop(!0, !0), i && t.datepicker._datepickerShowing && t.datepicker._hideDatepicker(t.datepicker._curInst.input[0])), s = t.datepicker._get(i, "beforeShow"), a = s ? s.apply(e, [e, i]) : {}, a !== !1 && (n(i.settings, a), i.lastVal = null, t.datepicker._lastInput = e, t.datepicker._setDateFromField(i), t.datepicker._inDialog && (e.value = ""), t.datepicker._pos || (t.datepicker._pos = t.datepicker._findPos(e), t.datepicker._pos[1] += e.offsetHeight), r = !1, t(e).parents().each(function () {
                return r |= "fixed" === t(this).css("position"), !r
            }), o = {left: t.datepicker._pos[0], top: t.datepicker._pos[1]}, t.datepicker._pos = null, i.dpDiv.empty(), i.dpDiv.css({position: "absolute", display: "block", top: "-1000px"}), t.datepicker._updateDatepicker(i), o = t.datepicker._checkOffset(i, o, r), i.dpDiv.css({position: t.datepicker._inDialog && t.blockUI ? "static" : r ? "fixed" : "absolute", display: "none", left: o.left + "px", top: o.top + "px"}), i.inline || (h = t.datepicker._get(i, "showAnim"), l = t.datepicker._get(i, "duration"), i.dpDiv.zIndex(t(e).zIndex() + 1), t.datepicker._datepickerShowing = !0, t.effects && t.effects.effect[h] ? i.dpDiv.show(h, t.datepicker._get(i, "showOptions"), l) : i.dpDiv[h || "show"](h ? l : null), i.input.is(":visible") && !i.input.is(":disabled") && i.input.focus(), t.datepicker._curInst = i))
        }
    }, _updateDatepicker: function (e) {
        this.maxRows = 4, a = e, e.dpDiv.empty().append(this._generateHTML(e)), this._attachHandlers(e), e.dpDiv.find("." + this._dayOverClass + " a").mouseover();
        var i, s = this._getNumberOfMonths(e), n = s[1], r = 17;
        e.dpDiv.removeClass("ui-datepicker-multi-2 ui-datepicker-multi-3 ui-datepicker-multi-4").width(""), n > 1 && e.dpDiv.addClass("ui-datepicker-multi-" + n).css("width", r * n + "em"), e.dpDiv[(1 !== s[0] || 1 !== s[1] ? "add" : "remove") + "Class"]("ui-datepicker-multi"), e.dpDiv[(this._get(e, "isRTL") ? "add" : "remove") + "Class"]("ui-datepicker-rtl"), e === t.datepicker._curInst && t.datepicker._datepickerShowing && e.input && e.input.is(":visible") && !e.input.is(":disabled") && e.input[0] !== document.activeElement && e.input.focus(), e.yearshtml && (i = e.yearshtml, setTimeout(function () {
            i === e.yearshtml && e.yearshtml && e.dpDiv.find("select.ui-datepicker-year:first").replaceWith(e.yearshtml), i = e.yearshtml = null
        }, 0))
    }, _getBorders: function (t) {
        var e = function (t) {
            return{thin: 1, medium: 2, thick: 3}[t] || t
        };
        return[parseFloat(e(t.css("border-left-width"))), parseFloat(e(t.css("border-top-width")))]
    }, _checkOffset: function (e, i, s) {
        var n = e.dpDiv.outerWidth(), a = e.dpDiv.outerHeight(), r = e.input ? e.input.outerWidth() : 0, o = e.input ? e.input.outerHeight() : 0, h = document.documentElement.clientWidth + (s ? 0 : t(document).scrollLeft()), l = document.documentElement.clientHeight + (s ? 0 : t(document).scrollTop());
        return i.left -= this._get(e, "isRTL") ? n - r : 0, i.left -= s && i.left === e.input.offset().left ? t(document).scrollLeft() : 0, i.top -= s && i.top === e.input.offset().top + o ? t(document).scrollTop() : 0, i.left -= Math.min(i.left, i.left + n > h && h > n ? Math.abs(i.left + n - h) : 0), i.top -= Math.min(i.top, i.top + a > l && l > a ? Math.abs(a + o) : 0), i
    }, _findPos: function (e) {
        for (var i, s = this._getInst(e), n = this._get(s, "isRTL"); e && ("hidden" === e.type || 1 !== e.nodeType || t.expr.filters.hidden(e));)e = e[n ? "previousSibling" : "nextSibling"];
        return i = t(e).offset(), [i.left, i.top]
    }, _hideDatepicker: function (e) {
        var i, s, n, a, o = this._curInst;
        !o || e && o !== t.data(e, r) || this._datepickerShowing && (i = this._get(o, "showAnim"), s = this._get(o, "duration"), n = function () {
            t.datepicker._tidyDialog(o)
        }, t.effects && (t.effects.effect[i] || t.effects[i]) ? o.dpDiv.hide(i, t.datepicker._get(o, "showOptions"), s, n) : o.dpDiv["slideDown" === i ? "slideUp" : "fadeIn" === i ? "fadeOut" : "hide"](i ? s : null, n), i || n(), this._datepickerShowing = !1, a = this._get(o, "onClose"), a && a.apply(o.input ? o.input[0] : null, [o.input ? o.input.val() : "", o]), this._lastInput = null, this._inDialog && (this._dialogInput.css({position: "absolute", left: "0", top: "-100px"}), t.blockUI && (t.unblockUI(), t("body").append(this.dpDiv))), this._inDialog = !1)
    }, _tidyDialog: function (t) {
        t.dpDiv.removeClass(this._dialogClass).unbind(".ui-datepicker-calendar")
    }, _checkExternalClick: function (e) {
        if (t.datepicker._curInst) {
            var i = t(e.target), s = t.datepicker._getInst(i[0]);
            (i[0].id !== t.datepicker._mainDivId && 0 === i.parents("#" + t.datepicker._mainDivId).length && !i.hasClass(t.datepicker.markerClassName) && !i.closest("." + t.datepicker._triggerClass).length && t.datepicker._datepickerShowing && (!t.datepicker._inDialog || !t.blockUI) || i.hasClass(t.datepicker.markerClassName) && t.datepicker._curInst !== s) && t.datepicker._hideDatepicker()
        }
    }, _adjustDate: function (e, i, s) {
        var n = t(e), a = this._getInst(n[0]);
        this._isDisabledDatepicker(n[0]) || (this._adjustInstDate(a, i + ("M" === s ? this._get(a, "showCurrentAtPos") : 0), s), this._updateDatepicker(a))
    }, _gotoToday: function (e) {
        var i, s = t(e), n = this._getInst(s[0]);
        this._get(n, "gotoCurrent") && n.currentDay ? (n.selectedDay = n.currentDay, n.drawMonth = n.selectedMonth = n.currentMonth, n.drawYear = n.selectedYear = n.currentYear) : (i = new Date, n.selectedDay = i.getDate(), n.drawMonth = n.selectedMonth = i.getMonth(), n.drawYear = n.selectedYear = i.getFullYear()), this._notifyChange(n), this._adjustDate(s)
    }, _selectMonthYear: function (e, i, s) {
        var n = t(e), a = this._getInst(n[0]);
        a["selected" + ("M" === s ? "Month" : "Year")] = a["draw" + ("M" === s ? "Month" : "Year")] = parseInt(i.options[i.selectedIndex].value, 10), this._notifyChange(a), this._adjustDate(n)
    }, _selectDay: function (e, i, s, n) {
        var a, r = t(e);
        t(n).hasClass(this._unselectableClass) || this._isDisabledDatepicker(r[0]) || (a = this._getInst(r[0]), a.selectedDay = a.currentDay = t("a", n).html(), a.selectedMonth = a.currentMonth = i, a.selectedYear = a.currentYear = s, this._selectDate(e, this._formatDate(a, a.currentDay, a.currentMonth, a.currentYear)))
    }, _clearDate: function (e) {
        var i = t(e);
        this._selectDate(i, "")
    }, _selectDate: function (e, i) {
        var s, n = t(e), a = this._getInst(n[0]);
        i = null != i ? i : this._formatDate(a), a.input && a.input.val(i), this._updateAlternate(a), s = this._get(a, "onSelect"), s ? s.apply(a.input ? a.input[0] : null, [i, a]) : a.input && a.input.trigger("change"), a.inline ? this._updateDatepicker(a) : (this._hideDatepicker(), this._lastInput = a.input[0], "object" != typeof a.input[0] && a.input.focus(), this._lastInput = null)
    }, _updateAlternate: function (e) {
        var i, s, n, a = this._get(e, "altField");
        a && (i = this._get(e, "altFormat") || this._get(e, "dateFormat"), s = this._getDate(e), n = this.formatDate(i, s, this._getFormatConfig(e)), t(a).each(function () {
            t(this).val(n)
        }))
    }, noWeekends: function (t) {
        var e = t.getDay();
        return[e > 0 && 6 > e, ""]
    }, iso8601Week: function (t) {
        var e, i = new Date(t.getTime());
        return i.setDate(i.getDate() + 4 - (i.getDay() || 7)), e = i.getTime(), i.setMonth(0), i.setDate(1), Math.floor(Math.round((e - i) / 864e5) / 7) + 1
    }, parseDate: function (i, s, n) {
        if (null == i || null == s)throw"Invalid arguments";
        if (s = "object" == typeof s ? "" + s : s + "", "" === s)return null;
        var a, r, o, h, l = 0, c = (n ? n.shortYearCutoff : null) || this._defaults.shortYearCutoff, u = "string" != typeof c ? c : (new Date).getFullYear() % 100 + parseInt(c, 10), d = (n ? n.dayNamesShort : null) || this._defaults.dayNamesShort, p = (n ? n.dayNames : null) || this._defaults.dayNames, f = (n ? n.monthNamesShort : null) || this._defaults.monthNamesShort, m = (n ? n.monthNames : null) || this._defaults.monthNames, g = -1, v = -1, _ = -1, b = -1, y = !1, w = function (t) {
            var e = i.length > a + 1 && i.charAt(a + 1) === t;
            return e && a++, e
        }, k = function (t) {
            var e = w(t), i = "@" === t ? 14 : "!" === t ? 20 : "y" === t && e ? 4 : "o" === t ? 3 : 2, n = RegExp("^\\d{1," + i + "}"), a = s.substring(l).match(n);
            if (!a)throw"Missing number at position " + l;
            return l += a[0].length, parseInt(a[0], 10)
        }, x = function (i, n, a) {
            var r = -1, o = t.map(w(i) ? a : n,function (t, e) {
                return[
                    [e, t]
                ]
            }).sort(function (t, e) {
                    return-(t[1].length - e[1].length)
                });
            if (t.each(o, function (t, i) {
                var n = i[1];
                return s.substr(l, n.length).toLowerCase() === n.toLowerCase() ? (r = i[0], l += n.length, !1) : e
            }), -1 !== r)return r + 1;
            throw"Unknown name at position " + l
        }, D = function () {
            if (s.charAt(l) !== i.charAt(a))throw"Unexpected literal at position " + l;
            l++
        };
        for (a = 0; i.length > a; a++)if (y)"'" !== i.charAt(a) || w("'") ? D() : y = !1; else switch (i.charAt(a)) {
            case"d":
                _ = k("d");
                break;
            case"D":
                x("D", d, p);
                break;
            case"o":
                b = k("o");
                break;
            case"m":
                v = k("m");
                break;
            case"M":
                v = x("M", f, m);
                break;
            case"y":
                g = k("y");
                break;
            case"@":
                h = new Date(k("@")), g = h.getFullYear(), v = h.getMonth() + 1, _ = h.getDate();
                break;
            case"!":
                h = new Date((k("!") - this._ticksTo1970) / 1e4), g = h.getFullYear(), v = h.getMonth() + 1, _ = h.getDate();
                break;
            case"'":
                w("'") ? D() : y = !0;
                break;
            default:
                D()
        }
        if (s.length > l && (o = s.substr(l), !/^\s+/.test(o)))throw"Extra/unparsed characters found in date: " + o;
        if (-1 === g ? g = (new Date).getFullYear() : 100 > g && (g += (new Date).getFullYear() - (new Date).getFullYear() % 100 + (u >= g ? 0 : -100)), b > -1)for (v = 1, _ = b; ;) {
            if (r = this._getDaysInMonth(g, v - 1), r >= _)break;
            v++, _ -= r
        }
        if (h = this._daylightSavingAdjust(new Date(g, v - 1, _)), h.getFullYear() !== g || h.getMonth() + 1 !== v || h.getDate() !== _)throw"Invalid date";
        return h
    }, ATOM: "yy-mm-dd", COOKIE: "D, dd M yy", ISO_8601: "yy-mm-dd", RFC_822: "D, d M y", RFC_850: "DD, dd-M-y", RFC_1036: "D, d M y", RFC_1123: "D, d M yy", RFC_2822: "D, d M yy", RSS: "D, d M y", TICKS: "!", TIMESTAMP: "@", W3C: "yy-mm-dd", _ticksTo1970: 1e7 * 60 * 60 * 24 * (718685 + Math.floor(492.5) - Math.floor(19.7) + Math.floor(4.925)), formatDate: function (t, e, i) {
        if (!e)return"";
        var s, n = (i ? i.dayNamesShort : null) || this._defaults.dayNamesShort, a = (i ? i.dayNames : null) || this._defaults.dayNames, r = (i ? i.monthNamesShort : null) || this._defaults.monthNamesShort, o = (i ? i.monthNames : null) || this._defaults.monthNames, h = function (e) {
            var i = t.length > s + 1 && t.charAt(s + 1) === e;
            return i && s++, i
        }, l = function (t, e, i) {
            var s = "" + e;
            if (h(t))for (; i > s.length;)s = "0" + s;
            return s
        }, c = function (t, e, i, s) {
            return h(t) ? s[e] : i[e]
        }, u = "", d = !1;
        if (e)for (s = 0; t.length > s; s++)if (d)"'" !== t.charAt(s) || h("'") ? u += t.charAt(s) : d = !1; else switch (t.charAt(s)) {
            case"d":
                u += l("d", e.getDate(), 2);
                break;
            case"D":
                u += c("D", e.getDay(), n, a);
                break;
            case"o":
                u += l("o", Math.round((new Date(e.getFullYear(), e.getMonth(), e.getDate()).getTime() - new Date(e.getFullYear(), 0, 0).getTime()) / 864e5), 3);
                break;
            case"m":
                u += l("m", e.getMonth() + 1, 2);
                break;
            case"M":
                u += c("M", e.getMonth(), r, o);
                break;
            case"y":
                u += h("y") ? e.getFullYear() : (10 > e.getYear() % 100 ? "0" : "") + e.getYear() % 100;
                break;
            case"@":
                u += e.getTime();
                break;
            case"!":
                u += 1e4 * e.getTime() + this._ticksTo1970;
                break;
            case"'":
                h("'") ? u += "'" : d = !0;
                break;
            default:
                u += t.charAt(s)
        }
        return u
    }, _possibleChars: function (t) {
        var e, i = "", s = !1, n = function (i) {
            var s = t.length > e + 1 && t.charAt(e + 1) === i;
            return s && e++, s
        };
        for (e = 0; t.length > e; e++)if (s)"'" !== t.charAt(e) || n("'") ? i += t.charAt(e) : s = !1; else switch (t.charAt(e)) {
            case"d":
            case"m":
            case"y":
            case"@":
                i += "0123456789";
                break;
            case"D":
            case"M":
                return null;
            case"'":
                n("'") ? i += "'" : s = !0;
                break;
            default:
                i += t.charAt(e)
        }
        return i
    }, _get: function (t, i) {
        return t.settings[i] !== e ? t.settings[i] : this._defaults[i]
    }, _setDateFromField: function (t, e) {
        if (t.input.val() !== t.lastVal) {
            var i = this._get(t, "dateFormat"), s = t.lastVal = t.input ? t.input.val() : null, n = this._getDefaultDate(t), a = n, r = this._getFormatConfig(t);
            try {
                a = this.parseDate(i, s, r) || n
            } catch (o) {
                s = e ? "" : s
            }
            t.selectedDay = a.getDate(), t.drawMonth = t.selectedMonth = a.getMonth(), t.drawYear = t.selectedYear = a.getFullYear(), t.currentDay = s ? a.getDate() : 0, t.currentMonth = s ? a.getMonth() : 0, t.currentYear = s ? a.getFullYear() : 0, this._adjustInstDate(t)
        }
    }, _getDefaultDate: function (t) {
        return this._restrictMinMax(t, this._determineDate(t, this._get(t, "defaultDate"), new Date))
    }, _determineDate: function (e, i, s) {
        var n = function (t) {
            var e = new Date;
            return e.setDate(e.getDate() + t), e
        }, a = function (i) {
            try {
                return t.datepicker.parseDate(t.datepicker._get(e, "dateFormat"), i, t.datepicker._getFormatConfig(e))
            } catch (s) {
            }
            for (var n = (i.toLowerCase().match(/^c/) ? t.datepicker._getDate(e) : null) || new Date, a = n.getFullYear(), r = n.getMonth(), o = n.getDate(), h = /([+\-]?[0-9]+)\s*(d|D|w|W|m|M|y|Y)?/g, l = h.exec(i); l;) {
                switch (l[2] || "d") {
                    case"d":
                    case"D":
                        o += parseInt(l[1], 10);
                        break;
                    case"w":
                    case"W":
                        o += 7 * parseInt(l[1], 10);
                        break;
                    case"m":
                    case"M":
                        r += parseInt(l[1], 10), o = Math.min(o, t.datepicker._getDaysInMonth(a, r));
                        break;
                    case"y":
                    case"Y":
                        a += parseInt(l[1], 10), o = Math.min(o, t.datepicker._getDaysInMonth(a, r))
                }
                l = h.exec(i)
            }
            return new Date(a, r, o)
        }, r = null == i || "" === i ? s : "string" == typeof i ? a(i) : "number" == typeof i ? isNaN(i) ? s : n(i) : new Date(i.getTime());
        return r = r && "Invalid Date" == "" + r ? s : r, r && (r.setHours(0), r.setMinutes(0), r.setSeconds(0), r.setMilliseconds(0)), this._daylightSavingAdjust(r)
    }, _daylightSavingAdjust: function (t) {
        return t ? (t.setHours(t.getHours() > 12 ? t.getHours() + 2 : 0), t) : null
    }, _setDate: function (t, e, i) {
        var s = !e, n = t.selectedMonth, a = t.selectedYear, r = this._restrictMinMax(t, this._determineDate(t, e, new Date));
        t.selectedDay = t.currentDay = r.getDate(), t.drawMonth = t.selectedMonth = t.currentMonth = r.getMonth(), t.drawYear = t.selectedYear = t.currentYear = r.getFullYear(), n === t.selectedMonth && a === t.selectedYear || i || this._notifyChange(t), this._adjustInstDate(t), t.input && t.input.val(s ? "" : this._formatDate(t))
    }, _getDate: function (t) {
        var e = !t.currentYear || t.input && "" === t.input.val() ? null : this._daylightSavingAdjust(new Date(t.currentYear, t.currentMonth, t.currentDay));
        return e
    }, _attachHandlers: function (e) {
        var i = this._get(e, "stepMonths"), s = "#" + e.id.replace(/\\\\/g, "\\");
        e.dpDiv.find("[data-handler]").map(function () {
            var e = {prev: function () {
                window["DP_jQuery_" + o].datepicker._adjustDate(s, -i, "M")
            }, next: function () {
                window["DP_jQuery_" + o].datepicker._adjustDate(s, +i, "M")
            }, hide: function () {
                window["DP_jQuery_" + o].datepicker._hideDatepicker()
            }, today: function () {
                window["DP_jQuery_" + o].datepicker._gotoToday(s)
            }, selectDay: function () {
                return window["DP_jQuery_" + o].datepicker._selectDay(s, +this.getAttribute("data-month"), +this.getAttribute("data-year"), this), !1
            }, selectMonth: function () {
                return window["DP_jQuery_" + o].datepicker._selectMonthYear(s, this, "M"), !1
            }, selectYear: function () {
                return window["DP_jQuery_" + o].datepicker._selectMonthYear(s, this, "Y"), !1
            }};
            t(this).bind(this.getAttribute("data-event"), e[this.getAttribute("data-handler")])
        })
    }, _generateHTML: function (t) {
        var e, i, s, n, a, r, o, h, l, c, u, d, p, f, m, g, v, _, b, y, w, k, x, D, T, C, S, M, N, I, P, A, z, H, E, F, O, W, j, R = new Date, L = this._daylightSavingAdjust(new Date(R.getFullYear(), R.getMonth(), R.getDate())), Y = this._get(t, "isRTL"), B = this._get(t, "showButtonPanel"), J = this._get(t, "hideIfNoPrevNext"), Q = this._get(t, "navigationAsDateFormat"), K = this._getNumberOfMonths(t), V = this._get(t, "showCurrentAtPos"), U = this._get(t, "stepMonths"), q = 1 !== K[0] || 1 !== K[1], X = this._daylightSavingAdjust(t.currentDay ? new Date(t.currentYear, t.currentMonth, t.currentDay) : new Date(9999, 9, 9)), G = this._getMinMaxDate(t, "min"), $ = this._getMinMaxDate(t, "max"), Z = t.drawMonth - V, te = t.drawYear;
        if (0 > Z && (Z += 12, te--), $)for (e = this._daylightSavingAdjust(new Date($.getFullYear(), $.getMonth() - K[0] * K[1] + 1, $.getDate())), e = G && G > e ? G : e; this._daylightSavingAdjust(new Date(te, Z, 1)) > e;)Z--, 0 > Z && (Z = 11, te--);
        for (t.drawMonth = Z, t.drawYear = te, i = this._get(t, "prevText"), i = Q ? this.formatDate(i, this._daylightSavingAdjust(new Date(te, Z - U, 1)), this._getFormatConfig(t)) : i, s = this._canAdjustMonth(t, -1, te, Z) ? "<a class='ui-datepicker-prev ui-corner-all' data-handler='prev' data-event='click' title='" + i + "'><span class='ui-icon ui-icon-circle-triangle-" + (Y ? "e" : "w") + "'>" + i + "</span></a>" : J ? "" : "<a class='ui-datepicker-prev ui-corner-all ui-state-disabled' title='" + i + "'><span class='ui-icon ui-icon-circle-triangle-" + (Y ? "e" : "w") + "'>" + i + "</span></a>", n = this._get(t, "nextText"), n = Q ? this.formatDate(n, this._daylightSavingAdjust(new Date(te, Z + U, 1)), this._getFormatConfig(t)) : n, a = this._canAdjustMonth(t, 1, te, Z) ? "<a class='ui-datepicker-next ui-corner-all' data-handler='next' data-event='click' title='" + n + "'><span class='ui-icon ui-icon-circle-triangle-" + (Y ? "w" : "e") + "'>" + n + "</span></a>" : J ? "" : "<a class='ui-datepicker-next ui-corner-all ui-state-disabled' title='" + n + "'><span class='ui-icon ui-icon-circle-triangle-" + (Y ? "w" : "e") + "'>" + n + "</span></a>", r = this._get(t, "currentText"), o = this._get(t, "gotoCurrent") && t.currentDay ? X : L, r = Q ? this.formatDate(r, o, this._getFormatConfig(t)) : r, h = t.inline ? "" : "<button type='button' class='ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all' data-handler='hide' data-event='click'>" + this._get(t, "closeText") + "</button>", l = B ? "<div class='ui-datepicker-buttonpane ui-widget-content'>" + (Y ? h : "") + (this._isInRange(t, o) ? "<button type='button' class='ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all' data-handler='today' data-event='click'>" + r + "</button>" : "") + (Y ? "" : h) + "</div>" : "", c = parseInt(this._get(t, "firstDay"), 10), c = isNaN(c) ? 0 : c, u = this._get(t, "showWeek"), d = this._get(t, "dayNames"), p = this._get(t, "dayNamesMin"), f = this._get(t, "monthNames"), m = this._get(t, "monthNamesShort"), g = this._get(t, "beforeShowDay"), v = this._get(t, "showOtherMonths"), _ = this._get(t, "selectOtherMonths"), b = this._getDefaultDate(t), y = "", k = 0; K[0] > k; k++) {
            for (x = "", this.maxRows = 4, D = 0; K[1] > D; D++) {
                if (T = this._daylightSavingAdjust(new Date(te, Z, t.selectedDay)), C = " ui-corner-all", S = "", q) {
                    if (S += "<div class='ui-datepicker-group", K[1] > 1)switch (D) {
                        case 0:
                            S += " ui-datepicker-group-first", C = " ui-corner-" + (Y ? "right" : "left");
                            break;
                        case K[1] - 1:
                            S += " ui-datepicker-group-last", C = " ui-corner-" + (Y ? "left" : "right");
                            break;
                        default:
                            S += " ui-datepicker-group-middle", C = ""
                    }
                    S += "'>"
                }
                for (S += "<div class='ui-datepicker-header ui-widget-header ui-helper-clearfix" + C + "'>" + (/all|left/.test(C) && 0 === k ? Y ? a : s : "") + (/all|right/.test(C) && 0 === k ? Y ? s : a : "") + this._generateMonthYearHeader(t, Z, te, G, $, k > 0 || D > 0, f, m) + "</div><table class='ui-datepicker-calendar'><thead>" + "<tr>", M = u ? "<th class='ui-datepicker-week-col'>" + this._get(t, "weekHeader") + "</th>" : "", w = 0; 7 > w; w++)N = (w + c) % 7, M += "<th" + ((w + c + 6) % 7 >= 5 ? " class='ui-datepicker-week-end'" : "") + ">" + "<span title='" + d[N] + "'>" + p[N] + "</span></th>";
                for (S += M + "</tr></thead><tbody>", I = this._getDaysInMonth(te, Z), te === t.selectedYear && Z === t.selectedMonth && (t.selectedDay = Math.min(t.selectedDay, I)), P = (this._getFirstDayOfMonth(te, Z) - c + 7) % 7, A = Math.ceil((P + I) / 7), z = q ? this.maxRows > A ? this.maxRows : A : A, this.maxRows = z, H = this._daylightSavingAdjust(new Date(te, Z, 1 - P)), E = 0; z > E; E++) {
                    for (S += "<tr>", F = u ? "<td class='ui-datepicker-week-col'>" + this._get(t, "calculateWeek")(H) + "</td>" : "", w = 0; 7 > w; w++)O = g ? g.apply(t.input ? t.input[0] : null, [H]) : [!0, ""], W = H.getMonth() !== Z, j = W && !_ || !O[0] || G && G > H || $ && H > $, F += "<td class='" + ((w + c + 6) % 7 >= 5 ? " ui-datepicker-week-end" : "") + (W ? " ui-datepicker-other-month" : "") + (H.getTime() === T.getTime() && Z === t.selectedMonth && t._keyEvent || b.getTime() === H.getTime() && b.getTime() === T.getTime() ? " " + this._dayOverClass : "") + (j ? " " + this._unselectableClass + " ui-state-disabled" : "") + (W && !v ? "" : " " + O[1] + (H.getTime() === X.getTime() ? " " + this._currentClass : "") + (H.getTime() === L.getTime() ? " ui-datepicker-today" : "")) + "'" + (W && !v || !O[2] ? "" : " title='" + O[2].replace(/'/g, "&#39;") + "'") + (j ? "" : " data-handler='selectDay' data-event='click' data-month='" + H.getMonth() + "' data-year='" + H.getFullYear() + "'") + ">" + (W && !v ? "&#xa0;" : j ? "<span class='ui-state-default'>" + H.getDate() + "</span>" : "<a class='ui-state-default" + (H.getTime() === L.getTime() ? " ui-state-highlight" : "") + (H.getTime() === X.getTime() ? " ui-state-active" : "") + (W ? " ui-priority-secondary" : "") + "' href='#'>" + H.getDate() + "</a>") + "</td>", H.setDate(H.getDate() + 1), H = this._daylightSavingAdjust(H);
                    S += F + "</tr>"
                }
                Z++, Z > 11 && (Z = 0, te++), S += "</tbody></table>" + (q ? "</div>" + (K[0] > 0 && D === K[1] - 1 ? "<div class='ui-datepicker-row-break'></div>" : "") : ""), x += S
            }
            y += x
        }
        return y += l, t._keyEvent = !1, y
    }, _generateMonthYearHeader: function (t, e, i, s, n, a, r, o) {
        var h, l, c, u, d, p, f, m, g = this._get(t, "changeMonth"), v = this._get(t, "changeYear"), _ = this._get(t, "showMonthAfterYear"), b = "<div class='ui-datepicker-title'>", y = "";
        if (a || !g)y += "<span class='ui-datepicker-month'>" + r[e] + "</span>"; else {
            for (h = s && s.getFullYear() === i, l = n && n.getFullYear() === i, y += "<select class='ui-datepicker-month' data-handler='selectMonth' data-event='change'>", c = 0; 12 > c; c++)(!h || c >= s.getMonth()) && (!l || n.getMonth() >= c) && (y += "<option value='" + c + "'" + (c === e ? " selected='selected'" : "") + ">" + o[c] + "</option>");
            y += "</select>"
        }
        if (_ || (b += y + (!a && g && v ? "" : "&#xa0;")), !t.yearshtml)if (t.yearshtml = "", a || !v)b += "<span class='ui-datepicker-year'>" + i + "</span>"; else {
            for (u = this._get(t, "yearRange").split(":"), d = (new Date).getFullYear(), p = function (t) {
                var e = t.match(/c[+\-].*/) ? i + parseInt(t.substring(1), 10) : t.match(/[+\-].*/) ? d + parseInt(t, 10) : parseInt(t, 10);
                return isNaN(e) ? d : e
            }, f = p(u[0]), m = Math.max(f, p(u[1] || "")), f = s ? Math.max(f, s.getFullYear()) : f, m = n ? Math.min(m, n.getFullYear()) : m, t.yearshtml += "<select class='ui-datepicker-year' data-handler='selectYear' data-event='change'>"; m >= f; f++)t.yearshtml += "<option value='" + f + "'" + (f === i ? " selected='selected'" : "") + ">" + f + "</option>";
            t.yearshtml += "</select>", b += t.yearshtml, t.yearshtml = null
        }
        return b += this._get(t, "yearSuffix"), _ && (b += (!a && g && v ? "" : "&#xa0;") + y), b += "</div>"
    }, _adjustInstDate: function (t, e, i) {
        var s = t.drawYear + ("Y" === i ? e : 0), n = t.drawMonth + ("M" === i ? e : 0), a = Math.min(t.selectedDay, this._getDaysInMonth(s, n)) + ("D" === i ? e : 0), r = this._restrictMinMax(t, this._daylightSavingAdjust(new Date(s, n, a)));
        t.selectedDay = r.getDate(), t.drawMonth = t.selectedMonth = r.getMonth(), t.drawYear = t.selectedYear = r.getFullYear(), ("M" === i || "Y" === i) && this._notifyChange(t)
    }, _restrictMinMax: function (t, e) {
        var i = this._getMinMaxDate(t, "min"), s = this._getMinMaxDate(t, "max"), n = i && i > e ? i : e;
        return s && n > s ? s : n
    }, _notifyChange: function (t) {
        var e = this._get(t, "onChangeMonthYear");
        e && e.apply(t.input ? t.input[0] : null, [t.selectedYear, t.selectedMonth + 1, t])
    }, _getNumberOfMonths: function (t) {
        var e = this._get(t, "numberOfMonths");
        return null == e ? [1, 1] : "number" == typeof e ? [1, e] : e
    }, _getMinMaxDate: function (t, e) {
        return this._determineDate(t, this._get(t, e + "Date"), null)
    }, _getDaysInMonth: function (t, e) {
        return 32 - this._daylightSavingAdjust(new Date(t, e, 32)).getDate()
    }, _getFirstDayOfMonth: function (t, e) {
        return new Date(t, e, 1).getDay()
    }, _canAdjustMonth: function (t, e, i, s) {
        var n = this._getNumberOfMonths(t), a = this._daylightSavingAdjust(new Date(i, s + (0 > e ? e : n[0] * n[1]), 1));
        return 0 > e && a.setDate(this._getDaysInMonth(a.getFullYear(), a.getMonth())), this._isInRange(t, a)
    }, _isInRange: function (t, e) {
        var i, s, n = this._getMinMaxDate(t, "min"), a = this._getMinMaxDate(t, "max"), r = null, o = null, h = this._get(t, "yearRange");
        return h && (i = h.split(":"), s = (new Date).getFullYear(), r = parseInt(i[0], 10), o = parseInt(i[1], 10), i[0].match(/[+\-].*/) && (r += s), i[1].match(/[+\-].*/) && (o += s)), (!n || e.getTime() >= n.getTime()) && (!a || e.getTime() <= a.getTime()) && (!r || e.getFullYear() >= r) && (!o || o >= e.getFullYear())
    }, _getFormatConfig: function (t) {
        var e = this._get(t, "shortYearCutoff");
        return e = "string" != typeof e ? e : (new Date).getFullYear() % 100 + parseInt(e, 10), {shortYearCutoff: e, dayNamesShort: this._get(t, "dayNamesShort"), dayNames: this._get(t, "dayNames"), monthNamesShort: this._get(t, "monthNamesShort"), monthNames: this._get(t, "monthNames")}
    }, _formatDate: function (t, e, i, s) {
        e || (t.currentDay = t.selectedDay, t.currentMonth = t.selectedMonth, t.currentYear = t.selectedYear);
        var n = e ? "object" == typeof e ? e : this._daylightSavingAdjust(new Date(s, i, e)) : this._daylightSavingAdjust(new Date(t.currentYear, t.currentMonth, t.currentDay));
        return this.formatDate(this._get(t, "dateFormat"), n, this._getFormatConfig(t))
    }}), t.fn.datepicker = function (e) {
        if (!this.length)return this;
        t.datepicker.initialized || (t(document).mousedown(t.datepicker._checkExternalClick), t.datepicker.initialized = !0), 0 === t("#" + t.datepicker._mainDivId).length && t("body").append(t.datepicker.dpDiv);
        var i = Array.prototype.slice.call(arguments, 1);
        return"string" != typeof e || "isDisabled" !== e && "getDate" !== e && "widget" !== e ? "option" === e && 2 === arguments.length && "string" == typeof arguments[1] ? t.datepicker["_" + e + "Datepicker"].apply(t.datepicker, [this[0]].concat(i)) : this.each(function () {
            "string" == typeof e ? t.datepicker["_" + e + "Datepicker"].apply(t.datepicker, [this].concat(i)) : t.datepicker._attachDatepicker(this, e)
        }) : t.datepicker["_" + e + "Datepicker"].apply(t.datepicker, [this[0]].concat(i))
    }, t.datepicker = new i, t.datepicker.initialized = !1, t.datepicker.uuid = (new Date).getTime(), t.datepicker.version = "1.10.2", window["DP_jQuery_" + o] = t
})(jQuery);
(function (t) {
    var e = {buttons: !0, height: !0, maxHeight: !0, maxWidth: !0, minHeight: !0, minWidth: !0, width: !0}, i = {maxHeight: !0, maxWidth: !0, minHeight: !0, minWidth: !0};
    t.widget("ui.dialog", {version: "1.10.2", options: {appendTo: "body", autoOpen: !0, buttons: [], closeOnEscape: !0, closeText: "close", dialogClass: "", draggable: !0, hide: null, height: "auto", maxHeight: null, maxWidth: null, minHeight: 150, minWidth: 150, modal: !1, position: {my: "center", at: "center", of: window, collision: "fit", using: function (e) {
        var i = t(this).css(e).offset().top;
        0 > i && t(this).css("top", e.top - i)
    }}, resizable: !0, show: null, title: null, width: 300, beforeClose: null, close: null, drag: null, dragStart: null, dragStop: null, focus: null, open: null, resize: null, resizeStart: null, resizeStop: null}, _create: function () {
        this.originalCss = {display: this.element[0].style.display, width: this.element[0].style.width, minHeight: this.element[0].style.minHeight, maxHeight: this.element[0].style.maxHeight, height: this.element[0].style.height}, this.originalPosition = {parent: this.element.parent(), index: this.element.parent().children().index(this.element)}, this.originalTitle = this.element.attr("title"), this.options.title = this.options.title || this.originalTitle, this._createWrapper(), this.element.show().removeAttr("title").addClass("ui-dialog-content ui-widget-content").appendTo(this.uiDialog), this._createTitlebar(), this._createButtonPane(), this.options.draggable && t.fn.draggable && this._makeDraggable(), this.options.resizable && t.fn.resizable && this._makeResizable(), this._isOpen = !1
    }, _init: function () {
        this.options.autoOpen && this.open()
    }, _appendTo: function () {
        var e = this.options.appendTo;
        return e && (e.jquery || e.nodeType) ? t(e) : this.document.find(e || "body").eq(0)
    }, _destroy: function () {
        var t, e = this.originalPosition;
        this._destroyOverlay(), this.element.removeUniqueId().removeClass("ui-dialog-content ui-widget-content").css(this.originalCss).detach(), this.uiDialog.stop(!0, !0).remove(), this.originalTitle && this.element.attr("title", this.originalTitle), t = e.parent.children().eq(e.index), t.length && t[0] !== this.element[0] ? t.before(this.element) : e.parent.append(this.element)
    }, widget: function () {
        return this.uiDialog
    }, disable: t.noop, enable: t.noop, close: function (e) {
        var i = this;
        this._isOpen && this._trigger("beforeClose", e) !== !1 && (this._isOpen = !1, this._destroyOverlay(), this.opener.filter(":focusable").focus().length || t(this.document[0].activeElement).blur(), this._hide(this.uiDialog, this.options.hide, function () {
            i._trigger("close", e)
        }))
    }, isOpen: function () {
        return this._isOpen
    }, moveToTop: function () {
        this._moveToTop()
    }, _moveToTop: function (t, e) {
        var i = !!this.uiDialog.nextAll(":visible").insertBefore(this.uiDialog).length;
        return i && !e && this._trigger("focus", t), i
    }, open: function () {
        var e = this;
        return this._isOpen ? (this._moveToTop() && this._focusTabbable(), undefined) : (this._isOpen = !0, this.opener = t(this.document[0].activeElement), this._size(), this._position(), this._createOverlay(), this._moveToTop(null, !0), this._show(this.uiDialog, this.options.show, function () {
            e._focusTabbable(), e._trigger("focus")
        }), this._trigger("open"), undefined)
    }, _focusTabbable: function () {
        var t = this.element.find("[autofocus]");
        t.length || (t = this.element.find(":tabbable")), t.length || (t = this.uiDialogButtonPane.find(":tabbable")), t.length || (t = this.uiDialogTitlebarClose.filter(":tabbable")), t.length || (t = this.uiDialog), t.eq(0).focus()
    }, _keepFocus: function (e) {
        function i() {
            var e = this.document[0].activeElement, i = this.uiDialog[0] === e || t.contains(this.uiDialog[0], e);
            i || this._focusTabbable()
        }

        e.preventDefault(), i.call(this), this._delay(i)
    }, _createWrapper: function () {
        this.uiDialog = t("<div>").addClass("ui-dialog ui-widget ui-widget-content ui-corner-all ui-front " + this.options.dialogClass).hide().attr({tabIndex: -1, role: "dialog"}).appendTo(this._appendTo()), this._on(this.uiDialog, {keydown: function (e) {
            if (this.options.closeOnEscape && !e.isDefaultPrevented() && e.keyCode && e.keyCode === t.ui.keyCode.ESCAPE)return e.preventDefault(), this.close(e), undefined;
            if (e.keyCode === t.ui.keyCode.TAB) {
                var i = this.uiDialog.find(":tabbable"), s = i.filter(":first"), n = i.filter(":last");
                e.target !== n[0] && e.target !== this.uiDialog[0] || e.shiftKey ? e.target !== s[0] && e.target !== this.uiDialog[0] || !e.shiftKey || (n.focus(1), e.preventDefault()) : (s.focus(1), e.preventDefault())
            }
        }, mousedown: function (t) {
            this._moveToTop(t) && this._focusTabbable()
        }}), this.element.find("[aria-describedby]").length || this.uiDialog.attr({"aria-describedby": this.element.uniqueId().attr("id")})
    }, _createTitlebar: function () {
        var e;
        this.uiDialogTitlebar = t("<div>").addClass("ui-dialog-titlebar ui-widget-header ui-corner-all ui-helper-clearfix").prependTo(this.uiDialog), this._on(this.uiDialogTitlebar, {mousedown: function (e) {
            t(e.target).closest(".ui-dialog-titlebar-close") || this.uiDialog.focus()
        }}), this.uiDialogTitlebarClose = t("<button></button>").button({label: this.options.closeText, icons: {primary: "ui-icon-closethick"}, text: !1}).addClass("ui-dialog-titlebar-close").appendTo(this.uiDialogTitlebar), this._on(this.uiDialogTitlebarClose, {click: function (t) {
            t.preventDefault(), this.close(t)
        }}), e = t("<span>").uniqueId().addClass("ui-dialog-title").prependTo(this.uiDialogTitlebar), this._title(e), this.uiDialog.attr({"aria-labelledby": e.attr("id")})
    }, _title: function (t) {
        this.options.title || t.html("&#160;"), t.text(this.options.title)
    }, _createButtonPane: function () {
        this.uiDialogButtonPane = t("<div>").addClass("ui-dialog-buttonpane ui-widget-content ui-helper-clearfix"), this.uiButtonSet = t("<div>").addClass("ui-dialog-buttonset").appendTo(this.uiDialogButtonPane), this._createButtons()
    }, _createButtons: function () {
        var e = this, i = this.options.buttons;
        return this.uiDialogButtonPane.remove(), this.uiButtonSet.empty(), t.isEmptyObject(i) || t.isArray(i) && !i.length ? (this.uiDialog.removeClass("ui-dialog-buttons"), undefined) : (t.each(i, function (i, s) {
            var n, a;
            s = t.isFunction(s) ? {click: s, text: i} : s, s = t.extend({type: "button"}, s), n = s.click, s.click = function () {
                n.apply(e.element[0], arguments)
            }, a = {icons: s.icons, text: s.showText}, delete s.icons, delete s.showText, t("<button></button>", s).button(a).appendTo(e.uiButtonSet)
        }), this.uiDialog.addClass("ui-dialog-buttons"), this.uiDialogButtonPane.appendTo(this.uiDialog), undefined)
    }, _makeDraggable: function () {
        function e(t) {
            return{position: t.position, offset: t.offset}
        }

        var i = this, s = this.options;
        this.uiDialog.draggable({cancel: ".ui-dialog-content, .ui-dialog-titlebar-close", handle: ".ui-dialog-titlebar", containment: "document", start: function (s, n) {
            t(this).addClass("ui-dialog-dragging"), i._blockFrames(), i._trigger("dragStart", s, e(n))
        }, drag: function (t, s) {
            i._trigger("drag", t, e(s))
        }, stop: function (n, a) {
            s.position = [a.position.left - i.document.scrollLeft(), a.position.top - i.document.scrollTop()], t(this).removeClass("ui-dialog-dragging"), i._unblockFrames(), i._trigger("dragStop", n, e(a))
        }})
    }, _makeResizable: function () {
        function e(t) {
            return{originalPosition: t.originalPosition, originalSize: t.originalSize, position: t.position, size: t.size}
        }

        var i = this, s = this.options, n = s.resizable, a = this.uiDialog.css("position"), o = "string" == typeof n ? n : "n,e,s,w,se,sw,ne,nw";
        this.uiDialog.resizable({cancel: ".ui-dialog-content", containment: "document", alsoResize: this.element, maxWidth: s.maxWidth, maxHeight: s.maxHeight, minWidth: s.minWidth, minHeight: this._minHeight(), handles: o, start: function (s, n) {
            t(this).addClass("ui-dialog-resizing"), i._blockFrames(), i._trigger("resizeStart", s, e(n))
        }, resize: function (t, s) {
            i._trigger("resize", t, e(s))
        }, stop: function (n, a) {
            s.height = t(this).height(), s.width = t(this).width(), t(this).removeClass("ui-dialog-resizing"), i._unblockFrames(), i._trigger("resizeStop", n, e(a))
        }}).css("position", a)
    }, _minHeight: function () {
        var t = this.options;
        return"auto" === t.height ? t.minHeight : Math.min(t.minHeight, t.height)
    }, _position: function () {
        var t = this.uiDialog.is(":visible");
        t || this.uiDialog.show(), this.uiDialog.position(this.options.position), t || this.uiDialog.hide()
    }, _setOptions: function (s) {
        var n = this, a = !1, o = {};
        t.each(s, function (t, s) {
            n._setOption(t, s), t in e && (a = !0), t in i && (o[t] = s)
        }), a && (this._size(), this._position()), this.uiDialog.is(":data(ui-resizable)") && this.uiDialog.resizable("option", o)
    }, _setOption: function (t, e) {
        var i, s, n = this.uiDialog;
        "dialogClass" === t && n.removeClass(this.options.dialogClass).addClass(e), "disabled" !== t && (this._super(t, e), "appendTo" === t && this.uiDialog.appendTo(this._appendTo()), "buttons" === t && this._createButtons(), "closeText" === t && this.uiDialogTitlebarClose.button({label: "" + e}), "draggable" === t && (i = n.is(":data(ui-draggable)"), i && !e && n.draggable("destroy"), !i && e && this._makeDraggable()), "position" === t && this._position(), "resizable" === t && (s = n.is(":data(ui-resizable)"), s && !e && n.resizable("destroy"), s && "string" == typeof e && n.resizable("option", "handles", e), s || e === !1 || this._makeResizable()), "title" === t && this._title(this.uiDialogTitlebar.find(".ui-dialog-title")))
    }, _size: function () {
        var t, e, i, s = this.options;
        this.element.show().css({width: "auto", minHeight: 0, maxHeight: "none", height: 0}), s.minWidth > s.width && (s.width = s.minWidth), t = this.uiDialog.css({height: "auto", width: s.width}).outerHeight(), e = Math.max(0, s.minHeight - t), i = "number" == typeof s.maxHeight ? Math.max(0, s.maxHeight - t) : "none", "auto" === s.height ? this.element.css({minHeight: e, maxHeight: i, height: "auto"}) : this.element.height(Math.max(0, s.height - t)), this.uiDialog.is(":data(ui-resizable)") && this.uiDialog.resizable("option", "minHeight", this._minHeight())
    }, _blockFrames: function () {
        this.iframeBlocks = this.document.find("iframe").map(function () {
            var e = t(this);
            return t("<div>").css({position: "absolute", width: e.outerWidth(), height: e.outerHeight()}).appendTo(e.parent()).offset(e.offset())[0]
        })
    }, _unblockFrames: function () {
        this.iframeBlocks && (this.iframeBlocks.remove(), delete this.iframeBlocks)
    }, _allowInteraction: function (e) {
        return t(e.target).closest(".ui-dialog").length ? !0 : !!t(e.target).closest(".ui-datepicker").length
    }, _createOverlay: function () {
        if (this.options.modal) {
            var e = this, i = this.widgetFullName;
            t.ui.dialog.overlayInstances || this._delay(function () {
                t.ui.dialog.overlayInstances && this.document.bind("focusin.dialog", function (s) {
                    e._allowInteraction(s) || (s.preventDefault(), t(".ui-dialog:visible:last .ui-dialog-content").data(i)._focusTabbable())
                })
            }), this.overlay = t("<div>").addClass("ui-widget-overlay ui-front").appendTo(this._appendTo()), this._on(this.overlay, {mousedown: "_keepFocus"}), t.ui.dialog.overlayInstances++
        }
    }, _destroyOverlay: function () {
        this.options.modal && this.overlay && (t.ui.dialog.overlayInstances--, t.ui.dialog.overlayInstances || this.document.unbind("focusin.dialog"), this.overlay.remove(), this.overlay = null)
    }}), t.ui.dialog.overlayInstances = 0, t.uiBackCompat !== !1 && t.widget("ui.dialog", t.ui.dialog, {_position: function () {
        var e, i = this.options.position, s = [], n = [0, 0];
        i ? (("string" == typeof i || "object" == typeof i && "0"in i) && (s = i.split ? i.split(" ") : [i[0], i[1]], 1 === s.length && (s[1] = s[0]), t.each(["left", "top"], function (t, e) {
            +s[t] === s[t] && (n[t] = s[t], s[t] = e)
        }), i = {my: s[0] + (0 > n[0] ? n[0] : "+" + n[0]) + " " + s[1] + (0 > n[1] ? n[1] : "+" + n[1]), at: s.join(" ")}), i = t.extend({}, t.ui.dialog.prototype.options.position, i)) : i = t.ui.dialog.prototype.options.position, e = this.uiDialog.is(":visible"), e || this.uiDialog.show(), this.uiDialog.position(i), e || this.uiDialog.hide()
    }})
})(jQuery);
(function (t) {
    t.widget("ui.menu", {version: "1.10.2", defaultElement: "<ul>", delay: 300, options: {icons: {submenu: "ui-icon-carat-1-e"}, menus: "ul", position: {my: "left top", at: "right top"}, role: "menu", blur: null, focus: null, select: null}, _create: function () {
        this.activeMenu = this.element, this.mouseHandled = !1, this.element.uniqueId().addClass("ui-menu ui-widget ui-widget-content ui-corner-all").toggleClass("ui-menu-icons", !!this.element.find(".ui-icon").length).attr({role: this.options.role, tabIndex: 0}).bind("click" + this.eventNamespace, t.proxy(function (t) {
            this.options.disabled && t.preventDefault()
        }, this)), this.options.disabled && this.element.addClass("ui-state-disabled").attr("aria-disabled", "true"), this._on({"mousedown .ui-menu-item > a": function (t) {
            t.preventDefault()
        }, "click .ui-state-disabled > a": function (t) {
            t.preventDefault()
        }, "click .ui-menu-item:has(a)": function (e) {
            var i = t(e.target).closest(".ui-menu-item");
            !this.mouseHandled && i.not(".ui-state-disabled").length && (this.mouseHandled = !0, this.select(e), i.has(".ui-menu").length ? this.expand(e) : this.element.is(":focus") || (this.element.trigger("focus", [!0]), this.active && 1 === this.active.parents(".ui-menu").length && clearTimeout(this.timer)))
        }, "mouseenter .ui-menu-item": function (e) {
            var i = t(e.currentTarget);
            i.siblings().children(".ui-state-active").removeClass("ui-state-active"), this.focus(e, i)
        }, mouseleave: "collapseAll", "mouseleave .ui-menu": "collapseAll", focus: function (t, e) {
            var i = this.active || this.element.children(".ui-menu-item").eq(0);
            e || this.focus(t, i)
        }, blur: function (e) {
            this._delay(function () {
                t.contains(this.element[0], this.document[0].activeElement) || this.collapseAll(e)
            })
        }, keydown: "_keydown"}), this.refresh(), this._on(this.document, {click: function (e) {
            t(e.target).closest(".ui-menu").length || this.collapseAll(e), this.mouseHandled = !1
        }})
    }, _destroy: function () {
        this.element.removeAttr("aria-activedescendant").find(".ui-menu").addBack().removeClass("ui-menu ui-widget ui-widget-content ui-corner-all ui-menu-icons").removeAttr("role").removeAttr("tabIndex").removeAttr("aria-labelledby").removeAttr("aria-expanded").removeAttr("aria-hidden").removeAttr("aria-disabled").removeUniqueId().show(), this.element.find(".ui-menu-item").removeClass("ui-menu-item").removeAttr("role").removeAttr("aria-disabled").children("a").removeUniqueId().removeClass("ui-corner-all ui-state-hover").removeAttr("tabIndex").removeAttr("role").removeAttr("aria-haspopup").children().each(function () {
            var e = t(this);
            e.data("ui-menu-submenu-carat") && e.remove()
        }), this.element.find(".ui-menu-divider").removeClass("ui-menu-divider ui-widget-content")
    }, _keydown: function (e) {
        function i(t) {
            return t.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&")
        }

        var s, n, a, o, r, h = !0;
        switch (e.keyCode) {
            case t.ui.keyCode.PAGE_UP:
                this.previousPage(e);
                break;
            case t.ui.keyCode.PAGE_DOWN:
                this.nextPage(e);
                break;
            case t.ui.keyCode.HOME:
                this._move("first", "first", e);
                break;
            case t.ui.keyCode.END:
                this._move("last", "last", e);
                break;
            case t.ui.keyCode.UP:
                this.previous(e);
                break;
            case t.ui.keyCode.DOWN:
                this.next(e);
                break;
            case t.ui.keyCode.LEFT:
                this.collapse(e);
                break;
            case t.ui.keyCode.RIGHT:
                this.active && !this.active.is(".ui-state-disabled") && this.expand(e);
                break;
            case t.ui.keyCode.ENTER:
            case t.ui.keyCode.SPACE:
                this._activate(e);
                break;
            case t.ui.keyCode.ESCAPE:
                this.collapse(e);
                break;
            default:
                h = !1, n = this.previousFilter || "", a = String.fromCharCode(e.keyCode), o = !1, clearTimeout(this.filterTimer), a === n ? o = !0 : a = n + a, r = RegExp("^" + i(a), "i"), s = this.activeMenu.children(".ui-menu-item").filter(function () {
                    return r.test(t(this).children("a").text())
                }), s = o && -1 !== s.index(this.active.next()) ? this.active.nextAll(".ui-menu-item") : s, s.length || (a = String.fromCharCode(e.keyCode), r = RegExp("^" + i(a), "i"), s = this.activeMenu.children(".ui-menu-item").filter(function () {
                    return r.test(t(this).children("a").text())
                })), s.length ? (this.focus(e, s), s.length > 1 ? (this.previousFilter = a, this.filterTimer = this._delay(function () {
                    delete this.previousFilter
                }, 1e3)) : delete this.previousFilter) : delete this.previousFilter
        }
        h && e.preventDefault()
    }, _activate: function (t) {
        this.active.is(".ui-state-disabled") || (this.active.children("a[aria-haspopup='true']").length ? this.expand(t) : this.select(t))
    }, refresh: function () {
        var e, i = this.options.icons.submenu, s = this.element.find(this.options.menus);
        s.filter(":not(.ui-menu)").addClass("ui-menu ui-widget ui-widget-content ui-corner-all").hide().attr({role: this.options.role, "aria-hidden": "true", "aria-expanded": "false"}).each(function () {
            var e = t(this), s = e.prev("a"), n = t("<span>").addClass("ui-menu-icon ui-icon " + i).data("ui-menu-submenu-carat", !0);
            s.attr("aria-haspopup", "true").prepend(n), e.attr("aria-labelledby", s.attr("id"))
        }), e = s.add(this.element), e.children(":not(.ui-menu-item):has(a)").addClass("ui-menu-item").attr("role", "presentation").children("a").uniqueId().addClass("ui-corner-all").attr({tabIndex: -1, role: this._itemRole()}), e.children(":not(.ui-menu-item)").each(function () {
            var e = t(this);
            /[^\-\u2014\u2013\s]/.test(e.text()) || e.addClass("ui-widget-content ui-menu-divider")
        }), e.children(".ui-state-disabled").attr("aria-disabled", "true"), this.active && !t.contains(this.element[0], this.active[0]) && this.blur()
    }, _itemRole: function () {
        return{menu: "menuitem", listbox: "option"}[this.options.role]
    }, _setOption: function (t, e) {
        "icons" === t && this.element.find(".ui-menu-icon").removeClass(this.options.icons.submenu).addClass(e.submenu), this._super(t, e)
    }, focus: function (t, e) {
        var i, s;
        this.blur(t, t && "focus" === t.type), this._scrollIntoView(e), this.active = e.first(), s = this.active.children("a").addClass("ui-state-focus"), this.options.role && this.element.attr("aria-activedescendant", s.attr("id")), this.active.parent().closest(".ui-menu-item").children("a:first").addClass("ui-state-active"), t && "keydown" === t.type ? this._close() : this.timer = this._delay(function () {
            this._close()
        }, this.delay), i = e.children(".ui-menu"), i.length && /^mouse/.test(t.type) && this._startOpening(i), this.activeMenu = e.parent(), this._trigger("focus", t, {item: e})
    }, _scrollIntoView: function (e) {
        var i, s, n, a, o, r;
        this._hasScroll() && (i = parseFloat(t.css(this.activeMenu[0], "borderTopWidth")) || 0, s = parseFloat(t.css(this.activeMenu[0], "paddingTop")) || 0, n = e.offset().top - this.activeMenu.offset().top - i - s, a = this.activeMenu.scrollTop(), o = this.activeMenu.height(), r = e.height(), 0 > n ? this.activeMenu.scrollTop(a + n) : n + r > o && this.activeMenu.scrollTop(a + n - o + r))
    }, blur: function (t, e) {
        e || clearTimeout(this.timer), this.active && (this.active.children("a").removeClass("ui-state-focus"), this.active = null, this._trigger("blur", t, {item: this.active}))
    }, _startOpening: function (t) {
        clearTimeout(this.timer), "true" === t.attr("aria-hidden") && (this.timer = this._delay(function () {
            this._close(), this._open(t)
        }, this.delay))
    }, _open: function (e) {
        var i = t.extend({of: this.active}, this.options.position);
        clearTimeout(this.timer), this.element.find(".ui-menu").not(e.parents(".ui-menu")).hide().attr("aria-hidden", "true"), e.show().removeAttr("aria-hidden").attr("aria-expanded", "true").position(i)
    }, collapseAll: function (e, i) {
        clearTimeout(this.timer), this.timer = this._delay(function () {
            var s = i ? this.element : t(e && e.target).closest(this.element.find(".ui-menu"));
            s.length || (s = this.element), this._close(s), this.blur(e), this.activeMenu = s
        }, this.delay)
    }, _close: function (t) {
        t || (t = this.active ? this.active.parent() : this.element), t.find(".ui-menu").hide().attr("aria-hidden", "true").attr("aria-expanded", "false").end().find("a.ui-state-active").removeClass("ui-state-active")
    }, collapse: function (t) {
        var e = this.active && this.active.parent().closest(".ui-menu-item", this.element);
        e && e.length && (this._close(), this.focus(t, e))
    }, expand: function (t) {
        var e = this.active && this.active.children(".ui-menu ").children(".ui-menu-item").first();
        e && e.length && (this._open(e.parent()), this._delay(function () {
            this.focus(t, e)
        }))
    }, next: function (t) {
        this._move("next", "first", t)
    }, previous: function (t) {
        this._move("prev", "last", t)
    }, isFirstItem: function () {
        return this.active && !this.active.prevAll(".ui-menu-item").length
    }, isLastItem: function () {
        return this.active && !this.active.nextAll(".ui-menu-item").length
    }, _move: function (t, e, i) {
        var s;
        this.active && (s = "first" === t || "last" === t ? this.active["first" === t ? "prevAll" : "nextAll"](".ui-menu-item").eq(-1) : this.active[t + "All"](".ui-menu-item").eq(0)), s && s.length && this.active || (s = this.activeMenu.children(".ui-menu-item")[e]()), this.focus(i, s)
    }, nextPage: function (e) {
        var i, s, n;
        return this.active ? (this.isLastItem() || (this._hasScroll() ? (s = this.active.offset().top, n = this.element.height(), this.active.nextAll(".ui-menu-item").each(function () {
            return i = t(this), 0 > i.offset().top - s - n
        }), this.focus(e, i)) : this.focus(e, this.activeMenu.children(".ui-menu-item")[this.active ? "last" : "first"]())), undefined) : (this.next(e), undefined)
    }, previousPage: function (e) {
        var i, s, n;
        return this.active ? (this.isFirstItem() || (this._hasScroll() ? (s = this.active.offset().top, n = this.element.height(), this.active.prevAll(".ui-menu-item").each(function () {
            return i = t(this), i.offset().top - s + n > 0
        }), this.focus(e, i)) : this.focus(e, this.activeMenu.children(".ui-menu-item").first())), undefined) : (this.next(e), undefined)
    }, _hasScroll: function () {
        return this.element.outerHeight() < this.element.prop("scrollHeight")
    }, select: function (e) {
        this.active = this.active || t(e.target).closest(".ui-menu-item");
        var i = {item: this.active};
        this.active.has(".ui-menu").length || this.collapseAll(e, !0), this._trigger("select", e, i)
    }})
})(jQuery);
(function (t, e) {
    t.widget("ui.progressbar", {version: "1.10.2", options: {max: 100, value: 0, change: null, complete: null}, min: 0, _create: function () {
        this.oldValue = this.options.value = this._constrainedValue(), this.element.addClass("ui-progressbar ui-widget ui-widget-content ui-corner-all").attr({role: "progressbar", "aria-valuemin": this.min}), this.valueDiv = t("<div class='ui-progressbar-value ui-widget-header ui-corner-left'></div>").appendTo(this.element), this._refreshValue()
    }, _destroy: function () {
        this.element.removeClass("ui-progressbar ui-widget ui-widget-content ui-corner-all").removeAttr("role").removeAttr("aria-valuemin").removeAttr("aria-valuemax").removeAttr("aria-valuenow"), this.valueDiv.remove()
    }, value: function (t) {
        return t === e ? this.options.value : (this.options.value = this._constrainedValue(t), this._refreshValue(), e)
    }, _constrainedValue: function (t) {
        return t === e && (t = this.options.value), this.indeterminate = t === !1, "number" != typeof t && (t = 0), this.indeterminate ? !1 : Math.min(this.options.max, Math.max(this.min, t))
    }, _setOptions: function (t) {
        var e = t.value;
        delete t.value, this._super(t), this.options.value = this._constrainedValue(e), this._refreshValue()
    }, _setOption: function (t, e) {
        "max" === t && (e = Math.max(this.min, e)), this._super(t, e)
    }, _percentage: function () {
        return this.indeterminate ? 100 : 100 * (this.options.value - this.min) / (this.options.max - this.min)
    }, _refreshValue: function () {
        var e = this.options.value, i = this._percentage();
        this.valueDiv.toggle(this.indeterminate || e > this.min).toggleClass("ui-corner-right", e === this.options.max).width(i.toFixed(0) + "%"), this.element.toggleClass("ui-progressbar-indeterminate", this.indeterminate), this.indeterminate ? (this.element.removeAttr("aria-valuenow"), this.overlayDiv || (this.overlayDiv = t("<div class='ui-progressbar-overlay'></div>").appendTo(this.valueDiv))) : (this.element.attr({"aria-valuemax": this.options.max, "aria-valuenow": e}), this.overlayDiv && (this.overlayDiv.remove(), this.overlayDiv = null)), this.oldValue !== e && (this.oldValue = e, this._trigger("change")), e === this.options.max && this._trigger("complete")
    }})
})(jQuery);
(function (t) {
    function e(t) {
        return function () {
            var e = this.element.val();
            t.apply(this, arguments), this._refresh(), e !== this.element.val() && this._trigger("change")
        }
    }

    t.widget("ui.spinner", {version: "1.10.2", defaultElement: "<input>", widgetEventPrefix: "spin", options: {culture: null, icons: {down: "ui-icon-triangle-1-s", up: "ui-icon-triangle-1-n"}, incremental: !0, max: null, min: null, numberFormat: null, page: 10, step: 1, change: null, spin: null, start: null, stop: null}, _create: function () {
        this._setOption("max", this.options.max), this._setOption("min", this.options.min), this._setOption("step", this.options.step), this._value(this.element.val(), !0), this._draw(), this._on(this._events), this._refresh(), this._on(this.window, {beforeunload: function () {
            this.element.removeAttr("autocomplete")
        }})
    }, _getCreateOptions: function () {
        var e = {}, i = this.element;
        return t.each(["min", "max", "step"], function (t, s) {
            var n = i.attr(s);
            void 0 !== n && n.length && (e[s] = n)
        }), e
    }, _events: {keydown: function (t) {
        this._start(t) && this._keydown(t) && t.preventDefault()
    }, keyup: "_stop", focus: function () {
        this.previous = this.element.val()
    }, blur: function (t) {
        return this.cancelBlur ? (delete this.cancelBlur, void 0) : (this._stop(), this._refresh(), this.previous !== this.element.val() && this._trigger("change", t), void 0)
    }, mousewheel: function (t, e) {
        if (e) {
            if (!this.spinning && !this._start(t))return!1;
            this._spin((e > 0 ? 1 : -1) * this.options.step, t), clearTimeout(this.mousewheelTimer), this.mousewheelTimer = this._delay(function () {
                this.spinning && this._stop(t)
            }, 100), t.preventDefault()
        }
    }, "mousedown .ui-spinner-button": function (e) {
        function i() {
            var t = this.element[0] === this.document[0].activeElement;
            t || (this.element.focus(), this.previous = s, this._delay(function () {
                this.previous = s
            }))
        }

        var s;
        s = this.element[0] === this.document[0].activeElement ? this.previous : this.element.val(), e.preventDefault(), i.call(this), this.cancelBlur = !0, this._delay(function () {
            delete this.cancelBlur, i.call(this)
        }), this._start(e) !== !1 && this._repeat(null, t(e.currentTarget).hasClass("ui-spinner-up") ? 1 : -1, e)
    }, "mouseup .ui-spinner-button": "_stop", "mouseenter .ui-spinner-button": function (e) {
        return t(e.currentTarget).hasClass("ui-state-active") ? this._start(e) === !1 ? !1 : (this._repeat(null, t(e.currentTarget).hasClass("ui-spinner-up") ? 1 : -1, e), void 0) : void 0
    }, "mouseleave .ui-spinner-button": "_stop"}, _draw: function () {
        var t = this.uiSpinner = this.element.addClass("ui-spinner-input").attr("autocomplete", "off").wrap(this._uiSpinnerHtml()).parent().append(this._buttonHtml());
        this.element.attr("role", "spinbutton"), this.buttons = t.find(".ui-spinner-button").attr("tabIndex", -1).button().removeClass("ui-corner-all"), this.buttons.height() > Math.ceil(.5 * t.height()) && t.height() > 0 && t.height(t.height()), this.options.disabled && this.disable()
    }, _keydown: function (e) {
        var i = this.options, s = t.ui.keyCode;
        switch (e.keyCode) {
            case s.UP:
                return this._repeat(null, 1, e), !0;
            case s.DOWN:
                return this._repeat(null, -1, e), !0;
            case s.PAGE_UP:
                return this._repeat(null, i.page, e), !0;
            case s.PAGE_DOWN:
                return this._repeat(null, -i.page, e), !0
        }
        return!1
    }, _uiSpinnerHtml: function () {
        return"<span class='ui-spinner ui-widget ui-widget-content ui-corner-all'></span>"
    }, _buttonHtml: function () {
        return"<a class='ui-spinner-button ui-spinner-up ui-corner-tr'><span class='ui-icon " + this.options.icons.up + "'>&#9650;</span>" + "</a>" + "<a class='ui-spinner-button ui-spinner-down ui-corner-br'>" + "<span class='ui-icon " + this.options.icons.down + "'>&#9660;</span>" + "</a>"
    }, _start: function (t) {
        return this.spinning || this._trigger("start", t) !== !1 ? (this.counter || (this.counter = 1), this.spinning = !0, !0) : !1
    }, _repeat: function (t, e, i) {
        t = t || 500, clearTimeout(this.timer), this.timer = this._delay(function () {
            this._repeat(40, e, i)
        }, t), this._spin(e * this.options.step, i)
    }, _spin: function (t, e) {
        var i = this.value() || 0;
        this.counter || (this.counter = 1), i = this._adjustValue(i + t * this._increment(this.counter)), this.spinning && this._trigger("spin", e, {value: i}) === !1 || (this._value(i), this.counter++)
    }, _increment: function (e) {
        var i = this.options.incremental;
        return i ? t.isFunction(i) ? i(e) : Math.floor(e * e * e / 5e4 - e * e / 500 + 17 * e / 200 + 1) : 1
    }, _precision: function () {
        var t = this._precisionOf(this.options.step);
        return null !== this.options.min && (t = Math.max(t, this._precisionOf(this.options.min))), t
    }, _precisionOf: function (t) {
        var e = "" + t, i = e.indexOf(".");
        return-1 === i ? 0 : e.length - i - 1
    }, _adjustValue: function (t) {
        var e, i, s = this.options;
        return e = null !== s.min ? s.min : 0, i = t - e, i = Math.round(i / s.step) * s.step, t = e + i, t = parseFloat(t.toFixed(this._precision())), null !== s.max && t > s.max ? s.max : null !== s.min && s.min > t ? s.min : t
    }, _stop: function (t) {
        this.spinning && (clearTimeout(this.timer), clearTimeout(this.mousewheelTimer), this.counter = 0, this.spinning = !1, this._trigger("stop", t))
    }, _setOption: function (t, e) {
        if ("culture" === t || "numberFormat" === t) {
            var i = this._parse(this.element.val());
            return this.options[t] = e, this.element.val(this._format(i)), void 0
        }
        ("max" === t || "min" === t || "step" === t) && "string" == typeof e && (e = this._parse(e)), "icons" === t && (this.buttons.first().find(".ui-icon").removeClass(this.options.icons.up).addClass(e.up), this.buttons.last().find(".ui-icon").removeClass(this.options.icons.down).addClass(e.down)), this._super(t, e), "disabled" === t && (e ? (this.element.prop("disabled", !0), this.buttons.button("disable")) : (this.element.prop("disabled", !1), this.buttons.button("enable")))
    }, _setOptions: e(function (t) {
        this._super(t), this._value(this.element.val())
    }), _parse: function (t) {
        return"string" == typeof t && "" !== t && (t = window.Globalize && this.options.numberFormat ? Globalize.parseFloat(t, 10, this.options.culture) : +t), "" === t || isNaN(t) ? null : t
    }, _format: function (t) {
        return"" === t ? "" : window.Globalize && this.options.numberFormat ? Globalize.format(t, this.options.numberFormat, this.options.culture) : t
    }, _refresh: function () {
        this.element.attr({"aria-valuemin": this.options.min, "aria-valuemax": this.options.max, "aria-valuenow": this._parse(this.element.val())})
    }, _value: function (t, e) {
        var i;
        "" !== t && (i = this._parse(t), null !== i && (e || (i = this._adjustValue(i)), t = this._format(i))), this.element.val(t), this._refresh()
    }, _destroy: function () {
        this.element.removeClass("ui-spinner-input").prop("disabled", !1).removeAttr("autocomplete").removeAttr("role").removeAttr("aria-valuemin").removeAttr("aria-valuemax").removeAttr("aria-valuenow"), this.uiSpinner.replaceWith(this.element)
    }, stepUp: e(function (t) {
        this._stepUp(t)
    }), _stepUp: function (t) {
        this._start() && (this._spin((t || 1) * this.options.step), this._stop())
    }, stepDown: e(function (t) {
        this._stepDown(t)
    }), _stepDown: function (t) {
        this._start() && (this._spin((t || 1) * -this.options.step), this._stop())
    }, pageUp: e(function (t) {
        this._stepUp((t || 1) * this.options.page)
    }), pageDown: e(function (t) {
        this._stepDown((t || 1) * this.options.page)
    }), value: function (t) {
        return arguments.length ? (e(this._value).call(this, t), void 0) : this._parse(this.element.val())
    }, widget: function () {
        return this.uiSpinner
    }})
})(jQuery);