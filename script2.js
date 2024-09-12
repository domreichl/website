document.querySelectorAll('.image-box').forEach(imageBox => {
    imageBox.addEventListener('click', function() {
        const list = document.createElement('ul');
        const items = ['Item 1', 'Item 2', 'Item 3'];

        // Create list items
        items.forEach(itemText => {
            const listItem = document.createElement('li');
            listItem.textContent = itemText;
            list.appendChild(listItem);
        });

        // Replace the image and overlay with the list
        this.innerHTML = '';
        this.appendChild(list);
    });
});
