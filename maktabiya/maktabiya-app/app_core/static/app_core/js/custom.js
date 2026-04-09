// admin UI Hack, force to change some items
(function() {
      var targetText = 'Maktabiya App';
      
    var navItems = document.querySelectorAll("li.nav-item a");
    for (var i = 0; i < navItems.length; i++) {
        if (navItems[i].innerText.trim() === targetText) {
            navItems[i].setAttribute('target', '_blank');
            break;
        }
    }
    
        
})();
(function() {
    var targetText = 'change';
    var targetHref = '/';  // Update this with the desired href value
    var selector = 'a.changelink[href="' + targetHref + '"]';
    var element = document.querySelector(selector);
  
    if (element && element.innerText.trim().toLowerCase() === targetText) {
        element.innerText = 'Go to the App';
        element.setAttribute('target', '_blank');
        // Remove the class "btn-info" and add the class "btn-dark"
        element.classList.remove("btn-info");
        element.classList.add("btn-dark");
    }
})();