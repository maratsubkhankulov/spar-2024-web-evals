import{options as r}from"./preact.mjs";var c,o,H,b,v=0,x=[],p=[],g=r.__b,A=r.__r,C=r.diffed,F=r.__c,q=r.unmount;function l(_,n){r.__h&&r.__h(o,_,v||n),v=0;var u=o.__H||(o.__H={__:[],__h:[]});return _>=u.__.length&&u.__.push({__V:p}),u.__[_]}function k(_){return v=1,B(U,_)}function B(_,n,u){var t=l(c++,2);if(t.t=_,!t.__c&&(t.__=[u?u(n):U(void 0,n),function(a){var f=t.__N?t.__N[0]:t.__[0],s=t.t(f,a);f!==s&&(t.__N=[s,t.__[1]],t.__c.setState({}))}],t.__c=o,!o.u)){var i=function(a,f,s){if(!t.__c.__H)return!0;var m=t.__c.__H.__.filter(function(e){return e.__c});if(m.every(function(e){return!e.__N}))return!h||h.call(this,a,f,s);var V=!1;return m.forEach(function(e){if(e.__N){var P=e.__[0];e.__=e.__N,e.__N=void 0,P!==e.__[0]&&(V=!0)}}),!(!V&&t.__c.props===a)&&(!h||h.call(this,a,f,s))};o.u=!0;var h=o.shouldComponentUpdate,N=o.componentWillUpdate;o.componentWillUpdate=function(a,f,s){if(this.__e){var m=h;h=void 0,i(a,f,s),h=m}N&&N.call(this,a,f,s)},o.shouldComponentUpdate=i}return t.__N||t.__}function j(_,n){var u=l(c++,3);!r.__s&&y(u.__H,n)&&(u.__=_,u.i=n,o.__H.__h.push(u))}function I(_,n){var u=l(c++,4);!r.__s&&y(u.__H,n)&&(u.__=_,u.i=n,o.__h.push(u))}function w(_){return v=5,T(function(){return{current:_}},[])}function z(_,n,u){v=6,I(function(){return typeof _=="function"?(_(n()),function(){return _(null)}):_?(_.current=n(),function(){return _.current=null}):void 0},u==null?u:u.concat(_))}function T(_,n){var u=l(c++,7);return y(u.__H,n)?(u.__V=_(),u.i=n,u.__h=_,u.__V):u.__}function L(_,n){return v=8,T(function(){return _},n)}function M(_){var n=o.context[_.__c],u=l(c++,9);return u.c=_,n?(u.__==null&&(u.__=!0,n.sub(o)),n.props.value):_.__}function G(_,n){r.useDebugValue&&r.useDebugValue(n?n(_):_)}function J(_){var n=l(c++,10),u=k();return n.__=_,o.componentDidCatch||(o.componentDidCatch=function(t,i){n.__&&n.__(t,i),u[1](t)}),[u[0],function(){u[1](void 0)}]}function K(){var _=l(c++,11);if(!_.__){for(var n=o.__v;n!==null&&!n.__m&&n.__!==null;)n=n.__;var u=n.__m||(n.__m=[0,0]);_.__="P"+u[0]+"-"+u[1]++}return _.__}function R(){for(var _;_=x.shift();)if(_.__P&&_.__H)try{_.__H.__h.forEach(d),_.__H.__h.forEach(E),_.__H.__h=[]}catch(n){_.__H.__h=[],r.__e(n,_.__v)}}r.__b=function(_){o=null,g&&g(_)},r.__r=function(_){A&&A(_),c=0;var n=(o=_.__c).__H;n&&(H===o?(n.__h=[],o.__h=[],n.__.forEach(function(u){u.__N&&(u.__=u.__N),u.__V=p,u.__N=u.i=void 0})):(n.__h.forEach(d),n.__h.forEach(E),n.__h=[],c=0)),H=o},r.diffed=function(_){C&&C(_);var n=_.__c;n&&n.__H&&(n.__H.__h.length&&(x.push(n)!==1&&b===r.requestAnimationFrame||((b=r.requestAnimationFrame)||S)(R)),n.__H.__.forEach(function(u){u.i&&(u.__H=u.i),u.__V!==p&&(u.__=u.__V),u.i=void 0,u.__V=p})),H=o=null},r.__c=function(_,n){n.some(function(u){try{u.__h.forEach(d),u.__h=u.__h.filter(function(t){return!t.__||E(t)})}catch(t){n.some(function(i){i.__h&&(i.__h=[])}),n=[],r.__e(t,u.__v)}}),F&&F(_,n)},r.unmount=function(_){q&&q(_);var n,u=_.__c;u&&u.__H&&(u.__H.__.forEach(function(t){try{d(t)}catch(i){n=i}}),u.__H=void 0,n&&r.__e(n,u.__v))};var D=typeof requestAnimationFrame=="function";function S(_){var n,u=function(){clearTimeout(t),D&&cancelAnimationFrame(n),setTimeout(_)},t=setTimeout(u,100);D&&(n=requestAnimationFrame(u))}function d(_){var n=o,u=_.__c;typeof u=="function"&&(_.__c=void 0,u()),o=n}function E(_){var n=o;_.__c=_.__(),o=n}function y(_,n){return!_||_.length!==n.length||n.some(function(u,t){return u!==_[t]})}function U(_,n){return typeof n=="function"?n(_):n}export{L as useCallback,M as useContext,G as useDebugValue,j as useEffect,J as useErrorBoundary,K as useId,z as useImperativeHandle,I as useLayoutEffect,T as useMemo,B as useReducer,w as useRef,k as useState};
