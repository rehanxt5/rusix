const headerSearchInputEle = document.getElementById('header-search');

headerSearchInputEle.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        const query = headerSearchInputEle.value.trim();
        if (query.length > 0) {
            fetch('http://localhost:1318/searchYoutube', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            })
            .then(response => response.json())
            .then(data => {
                // handle response data here
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }
});