function toggleContent(blockNumber) {
    // Get the corresponding content div by block number
    var content = document.getElementById('content-' + blockNumber);

    // Toggle the 'expanded' class to show or hide the content
    if (content.classList.contains('expanded')) {
        content.classList.remove('expanded');
    } else {
        content.classList.add('expanded');
    }
}
