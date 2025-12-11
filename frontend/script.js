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
                    <div class="search-video-container-item">
                        <img class="search-video-thumbnail" src="${video.thumbnail}" alt="${video.title}" width="20%" onclick="window.open('https://www.youtube.com/watch?v=${video.id}', '_blank')"/>
                        <div class="search-video-info">
                            <h3>${video.title}</h3>
                            <p>${video.channel}</p>
                        </div>
                        <div class="search-video-actions">
                            <div class="add-to-library-button"></div>
                            <button class="download-button" data-video-id="${video.id}">Download</button>
                        </div>
                    </div>
                    <style>
                        .search-video-container-item {
                            display: flex;
                            align-items: center;
                            margin-bottom: 2vh;
                            cursor: pointer;
                            gap: 1.5vw;
                        }
                        .search-video-thumbnail {
                            margin-right: 2vw;
                            border-radius: 1vw;
                        }
                        .search-video-info h3 {
                            margin: 0;
                            font-size: 2vh;
                            color: #fff;
                        }
                        .search-video-info p {
                            margin: 1vh 0 0 0;
                            font-size: 1.7vh;
                            color: #b3b3b3;
                        }
                        .search-video-actions {
                            display: flex;
                            align-items: center;
                            margin-left: auto;
                            gap: 1vw;
                        }
                        .add-to-library-button {
                            background-image: url('./assets/icons/add.svg');
                            width: 3vh;
                            height: 3vh;
                            background-size: cover;
                            cursor: pointer;
                        }
                        .add-to-library-button:hover {
                            background-image: url('./assets/icons/add-white.svg');
                        }
                        button {
                            padding: 0.5vh 2.5vw;
                            background-color: #7e5cf5;
                            color: white;
                            border: none;
                            border-radius: 2vw;
                            cursor: pointer;
                            font-size: 1.7vh;
                        }
                        button:hover {
                            background-color: #5a3ebf;
                        }
                    </style>
                `;
                   searchSectionEle.appendChild(videoEle);
                   
                   // Attach event listener after element is in DOM
                   const downloadBtn = videoEle.querySelector('.download-button');
                   downloadBtn.addEventListener('click', async (event) => {
                       event.stopPropagation();
                       const videoId = downloadBtn.getAttribute('data-video-id');
                       console.log('Download button clicked for video ID:', videoId);
                       
                       try {
                           const response = await fetch('http://localhost:1318/downloadYoutube', {
                               method: 'POST',
                               headers: {
                                   'Content-Type': 'application/json'
                               },
                               body: JSON.stringify({ videoId: videoId })
                           });
                           const result = await response.json();
                           console.log('Download response:', result);
                       } catch (error) {
                           console.error('Download error:', error);
                       }
                   }); 

                });
            })
            .catch(error => {
                console.error('Error:', error);
            });

            



        }
    }
});