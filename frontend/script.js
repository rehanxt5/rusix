const headerSearchInputEle = document.getElementById('header-search');
// Try id first, then fallback to class selector (HTML uses class="search-section")
const searchSectionEle = document.getElementById('search-section') || document.querySelector('.search-section');
const homeSectionEle = document.getElementById('home-section');
const librarySectionEle = document.getElementById('library-section');
if (!headerSearchInputEle) {
    console.warn('header-search input not found');
}
if (!searchSectionEle) {
    console.warn('search-section element not found');
}

headerSearchInputEle.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        const query = headerSearchInputEle ? headerSearchInputEle.value.trim() : '';
        if (query.length > 0) {
            if (searchSectionEle) {
                searchSectionEle.style.display = 'block';
            }
            if (homeSectionEle) {
                homeSectionEle.style.display = 'none';
            }
            if (librarySectionEle) {
                librarySectionEle.style.display = 'none';
            }
            // Clear previous search results
            if (searchSectionEle) {
                searchSectionEle.innerHTML = '';
            }

            // Send POST request to backend
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
                data.results.forEach(video => {
                   const videoEle = document.createElement('div');
                   videoEle.className = 'video-item';
                   videoEle.innerHTML = `
                        <div class="search-video-container-item" >
                            <img  class="search-video-thumbnail" src="${video.thumbnail}" alt="${video.title}" width="20%" onclick="window.open('https://www.youtube.com/watch?v=${video.id}', '_blank')"/>
                            <div class="search-video-info">
                                <h3>${video.title}</h3>
                                <p>${video.channel}</p>
                            </div>
                            <button>Download</button>
                        </div>
                        <style>
                            .search-video-container-item {
                                display: flex;
                                align-items: center;
                                margin-bottom: 15px;
                                cursor: pointer;
                                gap : 1.5vw;

                            }
                            
                            .search-video-thumbnail {
                                margin-right: 15px;
                                border-radius: 8px;
                            }
                            .search-video-info h3 {
                                margin: 0;
                                font-size: 16px;
                                color: #fff;
                            }
                            .search-video-info p {
                                margin: 5px 0 0 0;
                                font-size: 14px;
                                color: #b3b3b3;
                            }
                            button {
                                margin-left: auto;
                                padding: 8px 16px;
                                background-color: #1db954;
                                color: white;
                                border: none;
                                border-radius: 20px;
                                cursor: pointer;
                                font-size: 14px;
                            }
                            button:hover {
                                background-color: #1ed760;
                            }
                        </style>
                        <script>
                   `;
                   searchSectionEle.appendChild(videoEle); 

                });
            })
            .catch(error => {
                console.error('Error:', error);
            });

            



        }
    }
});