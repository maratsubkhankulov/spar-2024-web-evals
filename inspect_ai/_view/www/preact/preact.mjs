/* esm.sh - esbuild bundle(preact@10.19.5) es2022 production */
var D,a,Q,ne,x,z,X,$,Y,E={},O=[],oe=/acit|ex(?:s|g|n|p|$)|rph|grid|ows|mnc|ntw|ine[ch]|zoo|^ord|itera/i,F=Array.isArray;function b(e,_){for(var t in _)e[t]=_[t];return e}function Z(e){var _=e.parentNode;_&&_.removeChild(e)}function re(e,_,t){var r,n,i,l={};for(i in _)i=="key"?r=_[i]:i=="ref"?n=_[i]:l[i]=_[i];if(arguments.length>2&&(l.children=arguments.length>3?D.call(arguments,2):t),typeof e=="function"&&e.defaultProps!=null)for(i in e.defaultProps)l[i]===void 0&&(l[i]=e.defaultProps[i]);return S(e,l,r,n,null)}function S(e,_,t,r,n){var i={type:e,props:_,key:t,ref:r,__k:null,__:null,__b:0,__e:null,__d:void 0,__c:null,constructor:void 0,__v:n??++Q,__i:-1,__u:0};return n==null&&a.vnode!=null&&a.vnode(i),i}function de(){return{current:null}}function H(e){return e.children}function W(e,_){this.props=e,this.context=_}function w(e,_){if(_==null)return e.__?w(e.__,e.__i+1):null;for(var t;_<e.__k.length;_++)if((t=e.__k[_])!=null&&t.__e!=null)return t.__e;return typeof e.type=="function"?w(e):null}function ie(e,_,t){var r,n=e.__v,i=n.__e,l=e.__P;if(l)return(r=b({},n)).__v=n.__v+1,a.vnode&&a.vnode(r),G(l,r,n,e.__n,l.ownerSVGElement!==void 0,32&n.__u?[i]:null,_,i??w(n),!!(32&n.__u),t),r.__v=n.__v,r.__.__k[r.__i]=r,r.__d=void 0,r.__e!=i&&ee(r),r}function ee(e){var _,t;if((e=e.__)!=null&&e.__c!=null){for(e.__e=e.__c.base=null,_=0;_<e.__k.length;_++)if((t=e.__k[_])!=null&&t.__e!=null){e.__e=e.__c.base=t.__e;break}return ee(e)}}function I(e){(!e.__d&&(e.__d=!0)&&x.push(e)&&!A.__r++||z!==a.debounceRendering)&&((z=a.debounceRendering)||X)(A)}function A(){var e,_,t,r=[],n=[];for(x.sort($);e=x.shift();)e.__d&&(t=x.length,_=ie(e,r,n)||_,t===0||x.length>t?(R(r,_,n),n.length=r.length=0,_=void 0,x.sort($)):_&&a.__c&&a.__c(_,O));_&&R(r,_,n),A.__r=0}function _e(e,_,t,r,n,i,l,u,c,s,p){var o,m,f,h,k,v=r&&r.__k||O,d=_.length;for(t.__d=c,le(t,_,v),c=t.__d,o=0;o<d;o++)(f=t.__k[o])!=null&&typeof f!="boolean"&&typeof f!="function"&&(m=f.__i===-1?E:v[f.__i]||E,f.__i=o,G(e,f,m,n,i,l,u,c,s,p),h=f.__e,f.ref&&m.ref!=f.ref&&(m.ref&&V(m.ref,null,f),p.push(f.ref,f.__c||h,f)),k==null&&h!=null&&(k=h),65536&f.__u||m.__k===f.__k?c=te(f,c,e):typeof f.type=="function"&&f.__d!==void 0?c=f.__d:h&&(c=h.nextSibling),f.__d=void 0,f.__u&=-196609);t.__d=c,t.__e=k}function le(e,_,t){var r,n,i,l,u,c=_.length,s=t.length,p=s,o=0;for(e.__k=[],r=0;r<c;r++)(n=e.__k[r]=(n=_[r])==null||typeof n=="boolean"||typeof n=="function"?null:typeof n=="string"||typeof n=="number"||typeof n=="bigint"||n.constructor==String?S(null,n,null,null,n):F(n)?S(H,{children:n},null,null,null):n.constructor===void 0&&n.__b>0?S(n.type,n.props,n.key,n.ref?n.ref:null,n.__v):n)!=null?(n.__=e,n.__b=e.__b+1,u=ue(n,t,l=r+o,p),n.__i=u,i=null,u!==-1&&(p--,(i=t[u])&&(i.__u|=131072)),i==null||i.__v===null?(u==-1&&o--,typeof n.type!="function"&&(n.__u|=65536)):u!==l&&(u===l+1?o++:u>l?p>c-l?o+=u-l:o--:o=u<l&&u==l-1?u-l:0,u!==r+o&&(n.__u|=65536))):(i=t[r])&&i.key==null&&i.__e&&!(131072&i.__u)&&(i.__e==e.__d&&(e.__d=w(i)),B(i,i,!1),t[r]=null,p--);if(p)for(r=0;r<s;r++)(i=t[r])!=null&&!(131072&i.__u)&&(i.__e==e.__d&&(e.__d=w(i)),B(i,i))}function te(e,_,t){var r,n;if(typeof e.type=="function"){for(r=e.__k,n=0;r&&n<r.length;n++)r[n]&&(r[n].__=e,_=te(r[n],_,t));return _}e.__e!=_&&(t.insertBefore(e.__e,_||null),_=e.__e);do _=_&&_.nextSibling;while(_!=null&&_.nodeType===8);return _}function se(e,_){return _=_||[],e==null||typeof e=="boolean"||(F(e)?e.some(function(t){se(t,_)}):_.push(e)),_}function ue(e,_,t,r){var n=e.key,i=e.type,l=t-1,u=t+1,c=_[t];if(c===null||c&&n==c.key&&i===c.type)return t;if(r>(c!=null&&!(131072&c.__u)?1:0))for(;l>=0||u<_.length;){if(l>=0){if((c=_[l])&&!(131072&c.__u)&&n==c.key&&i===c.type)return l;l--}if(u<_.length){if((c=_[u])&&!(131072&c.__u)&&n==c.key&&i===c.type)return u;u++}}return-1}function q(e,_,t){_[0]==="-"?e.setProperty(_,t??""):e[_]=t==null?"":typeof t!="number"||oe.test(_)?t:t+"px"}function M(e,_,t,r,n){var i;e:if(_==="style")if(typeof t=="string")e.style.cssText=t;else{if(typeof r=="string"&&(e.style.cssText=r=""),r)for(_ in r)t&&_ in t||q(e.style,_,"");if(t)for(_ in t)r&&t[_]===r[_]||q(e.style,_,t[_])}else if(_[0]==="o"&&_[1]==="n")i=_!==(_=_.replace(/(PointerCapture)$|Capture$/i,"$1")),_=_.toLowerCase()in e?_.toLowerCase().slice(2):_.slice(2),e.l||(e.l={}),e.l[_+i]=t,t?r?t.u=r.u:(t.u=Date.now(),e.addEventListener(_,i?K:J,i)):e.removeEventListener(_,i?K:J,i);else{if(n)_=_.replace(/xlink(H|:h)/,"h").replace(/sName$/,"s");else if(_!=="width"&&_!=="height"&&_!=="href"&&_!=="list"&&_!=="form"&&_!=="tabIndex"&&_!=="download"&&_!=="rowSpan"&&_!=="colSpan"&&_!=="role"&&_ in e)try{e[_]=t??"";break e}catch{}typeof t=="function"||(t==null||t===!1&&_[4]!=="-"?e.removeAttribute(_):e.setAttribute(_,t))}}function J(e){if(this.l){var _=this.l[e.type+!1];if(e.t){if(e.t<=_.u)return}else e.t=Date.now();return _(a.event?a.event(e):e)}}function K(e){if(this.l)return this.l[e.type+!0](a.event?a.event(e):e)}function G(e,_,t,r,n,i,l,u,c,s){var p,o,m,f,h,k,v,d,y,C,T,P,j,U,N,g=_.type;if(_.constructor!==void 0)return null;128&t.__u&&(c=!!(32&t.__u),i=[u=_.__e=t.__e]),(p=a.__b)&&p(_);e:if(typeof g=="function")try{if(d=_.props,y=(p=g.contextType)&&r[p.__c],C=p?y?y.props.value:p.__:r,t.__c?v=(o=_.__c=t.__c).__=o.__E:("prototype"in g&&g.prototype.render?_.__c=o=new g(d,C):(_.__c=o=new W(d,C),o.constructor=g,o.render=ce),y&&y.sub(o),o.props=d,o.state||(o.state={}),o.context=C,o.__n=r,m=o.__d=!0,o.__h=[],o._sb=[]),o.__s==null&&(o.__s=o.state),g.getDerivedStateFromProps!=null&&(o.__s==o.state&&(o.__s=b({},o.__s)),b(o.__s,g.getDerivedStateFromProps(d,o.__s))),f=o.props,h=o.state,o.__v=_,m)g.getDerivedStateFromProps==null&&o.componentWillMount!=null&&o.componentWillMount(),o.componentDidMount!=null&&o.__h.push(o.componentDidMount);else{if(g.getDerivedStateFromProps==null&&d!==f&&o.componentWillReceiveProps!=null&&o.componentWillReceiveProps(d,C),!o.__e&&(o.shouldComponentUpdate!=null&&o.shouldComponentUpdate(d,o.__s,C)===!1||_.__v===t.__v)){for(_.__v!==t.__v&&(o.props=d,o.state=o.__s,o.__d=!1),_.__e=t.__e,_.__k=t.__k,_.__k.forEach(function(L){L&&(L.__=_)}),T=0;T<o._sb.length;T++)o.__h.push(o._sb[T]);o._sb=[],o.__h.length&&l.push(o);break e}o.componentWillUpdate!=null&&o.componentWillUpdate(d,o.__s,C),o.componentDidUpdate!=null&&o.__h.push(function(){o.componentDidUpdate(f,h,k)})}if(o.context=C,o.props=d,o.__P=e,o.__e=!1,P=a.__r,j=0,"prototype"in g&&g.prototype.render){for(o.state=o.__s,o.__d=!1,P&&P(_),p=o.render(o.props,o.state,o.context),U=0;U<o._sb.length;U++)o.__h.push(o._sb[U]);o._sb=[]}else do o.__d=!1,P&&P(_),p=o.render(o.props,o.state,o.context),o.state=o.__s;while(o.__d&&++j<25);o.state=o.__s,o.getChildContext!=null&&(r=b(b({},r),o.getChildContext())),m||o.getSnapshotBeforeUpdate==null||(k=o.getSnapshotBeforeUpdate(f,h)),_e(e,F(N=p!=null&&p.type===H&&p.key==null?p.props.children:p)?N:[N],_,t,r,n,i,l,u,c,s),o.base=_.__e,_.__u&=-161,o.__h.length&&l.push(o),v&&(o.__E=o.__=null)}catch(L){_.__v=null,c||i!=null?(_.__e=u,_.__u|=c?160:32,i[i.indexOf(u)]=null):(_.__e=t.__e,_.__k=t.__k),a.__e(L,_,t)}else i==null&&_.__v===t.__v?(_.__k=t.__k,_.__e=t.__e):_.__e=fe(t.__e,_,t,r,n,i,l,c,s);(p=a.diffed)&&p(_)}function R(e,_,t){for(var r=0;r<t.length;r++)V(t[r],t[++r],t[++r]);a.__c&&a.__c(_,e),e.some(function(n){try{e=n.__h,n.__h=[],e.some(function(i){i.call(n)})}catch(i){a.__e(i,n.__v)}})}function fe(e,_,t,r,n,i,l,u,c){var s,p,o,m,f,h,k,v=t.props,d=_.props,y=_.type;if(y==="svg"&&(n=!0),i!=null){for(s=0;s<i.length;s++)if((f=i[s])&&"setAttribute"in f==!!y&&(y?f.localName===y:f.nodeType===3)){e=f,i[s]=null;break}}if(e==null){if(y===null)return document.createTextNode(d);e=n?document.createElementNS("http://www.w3.org/2000/svg",y):document.createElement(y,d.is&&d),i=null,u=!1}if(y===null)v===d||u&&e.data===d||(e.data=d);else{if(i=i&&D.call(e.childNodes),v=t.props||E,!u&&i!=null)for(v={},s=0;s<e.attributes.length;s++)v[(f=e.attributes[s]).name]=f.value;for(s in v)f=v[s],s=="children"||(s=="dangerouslySetInnerHTML"?o=f:s==="key"||s in d||M(e,s,null,f,n));for(s in d)f=d[s],s=="children"?m=f:s=="dangerouslySetInnerHTML"?p=f:s=="value"?h=f:s=="checked"?k=f:s==="key"||u&&typeof f!="function"||v[s]===f||M(e,s,f,v[s],n);if(p)u||o&&(p.__html===o.__html||p.__html===e.innerHTML)||(e.innerHTML=p.__html),_.__k=[];else if(o&&(e.innerHTML=""),_e(e,F(m)?m:[m],_,t,r,n&&y!=="foreignObject",i,l,i?i[0]:t.__k&&w(t,0),u,c),i!=null)for(s=i.length;s--;)i[s]!=null&&Z(i[s]);u||(s="value",h!==void 0&&(h!==e[s]||y==="progress"&&!h||y==="option"&&h!==v[s])&&M(e,s,h,v[s],!1),s="checked",k!==void 0&&k!==e[s]&&M(e,s,k,v[s],!1))}return e}function V(e,_,t){try{typeof e=="function"?e(_):e.current=_}catch(r){a.__e(r,t)}}function B(e,_,t){var r,n;if(a.unmount&&a.unmount(e),(r=e.ref)&&(r.current&&r.current!==e.__e||V(r,null,_)),(r=e.__c)!=null){if(r.componentWillUnmount)try{r.componentWillUnmount()}catch(i){a.__e(i,_)}r.base=r.__P=null,e.__c=void 0}if(r=e.__k)for(n=0;n<r.length;n++)r[n]&&B(r[n],_,t||typeof e.type!="function");t||e.__e==null||Z(e.__e),e.__=e.__e=e.__d=void 0}function ce(e,_,t){return this.constructor(e,t)}function pe(e,_,t){var r,n,i,l;a.__&&a.__(e,_),n=(r=typeof t=="function")?null:t&&t.__k||_.__k,i=[],l=[],G(_,e=(!r&&t||_).__k=re(H,null,[e]),n||E,E,_.ownerSVGElement!==void 0,!r&&t?[t]:n?null:_.firstChild?D.call(_.childNodes):null,i,!r&&t?t:n?n.__e:_.firstChild,r,l),e.__d=void 0,R(i,e,l)}function ae(e,_){pe(e,_,ae)}function he(e,_,t){var r,n,i,l,u=b({},e.props);for(i in e.type&&e.type.defaultProps&&(l=e.type.defaultProps),_)i=="key"?r=_[i]:i=="ref"?n=_[i]:u[i]=_[i]===void 0&&l!==void 0?l[i]:_[i];return arguments.length>2&&(u.children=arguments.length>3?D.call(arguments,2):t),S(e.type,u,r||e.key,n||e.ref,null)}function ve(e,_){var t={__c:_="__cC"+Y++,__:e,Consumer:function(r,n){return r.children(n)},Provider:function(r){var n,i;return this.getChildContext||(n=[],(i={})[_]=this,this.getChildContext=function(){return i},this.shouldComponentUpdate=function(l){this.props.value!==l.value&&n.some(function(u){u.__e=!0,I(u)})},this.sub=function(l){n.push(l);var u=l.componentWillUnmount;l.componentWillUnmount=function(){n.splice(n.indexOf(l),1),u&&u.call(l)}}),r.children}};return t.Provider.__=t.Consumer.contextType=t}D=O.slice,a={__e:function(e,_,t,r){for(var n,i,l;_=_.__;)if((n=_.__c)&&!n.__)try{if((i=n.constructor)&&i.getDerivedStateFromError!=null&&(n.setState(i.getDerivedStateFromError(e)),l=n.__d),n.componentDidCatch!=null&&(n.componentDidCatch(e,r||{}),l=n.__d),l)return n.__E=n}catch(u){e=u}throw e}},Q=0,ne=function(e){return e!=null&&e.constructor==null},W.prototype.setState=function(e,_){var t;t=this.__s!=null&&this.__s!==this.state?this.__s:this.__s=b({},this.state),typeof e=="function"&&(e=e(b({},t),this.props)),e&&b(t,e),e!=null&&this.__v&&(_&&this._sb.push(_),I(this))},W.prototype.forceUpdate=function(e){this.__v&&(this.__e=!0,e&&this.__h.push(e),I(this))},W.prototype.render=H,x=[],X=typeof Promise=="function"?Promise.prototype.then.bind(Promise.resolve()):setTimeout,$=function(e,_){return e.__v.__b-_.__v.__b},A.__r=0,Y=0;export{W as Component,H as Fragment,he as cloneElement,ve as createContext,re as createElement,de as createRef,re as h,ae as hydrate,ne as isValidElement,a as options,pe as render,se as toChildArray};
