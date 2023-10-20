function hexify() {
    document.querySelectorAll('div').forEach(e => {

        // Only check divs which have no children or are of the class px-1.
        // This covers most of the relevant binary strings to convert.
        if ((e.children.length == 0) || (e.classList.contains('px-1'))) {

            // Match binary strings of length 32
            [...e.innerText.matchAll(/[01]{32}/g)].forEach(match => {

                // Replace with hexidecimal representation.
                e.innerText = parseInt(match, 2).toString(16).padStart(8, '0'); 
            });
        }
    });
};