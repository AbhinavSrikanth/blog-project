// Function to fetch user-generated posts
async function fetchUserGeneratedPosts() {
    try {
        const url='/user-posts';
        const response=await fetch(url);
        if (!response.ok) {
            throw new Error(`Failed to fetch user-generated posts. Status: ${response.status}`);
        }
        const data = await response.json();
        return data.posts;
    } catch (error) {
        console.error(`Error Fetching user-generated posts:${error}`);
        return [];
    }
  }
  
  // Function to get random user-generated posts
  function getRandomUserGeneratedPosts(posts, count) {
    const randomPosts = [];
    const shuffledPosts = [...posts];
    shuffledPosts.sort(() => Math.random() - 0.5);
  
    for (let i = 0; i < count; i++) {
        if (i < shuffledPosts.length) {
            randomPosts.push(shuffledPosts[i]);
        } else {
            break;
        }
    }
  
    return randomPosts;
  }
  async function renderPosts() {
    try {
      const posts = await fetchUserGeneratedPosts();
      console.log(posts)
      if (posts && posts.length > 0) {
        const postContainer = document.getElementById('postContainer');
        postContainer.innerHTML = '';
        posts.forEach((post) => {
        const postDiv = document.createElement('div');
        postDiv.classList.add('post');

        const titleElement = document.createElement('h2');
        titleElement.textContent = post.title;
        const readMoreLink=document.createElement('a');
        readMoreLink.href=`/post_details/${post.id}`;
        readMoreLink.textContent='Read More';
        postDiv.appendChild(titleElement);
        postDiv.appendChild(readMoreLink);
        postContainer.appendChild(postDiv);
      });
      } else {
        console.log("No posts available");
      }
    } catch (error) {
      console.error("Error fetching or rendering posts:", error);
    }
  }
//   // Function to display random user-generated posts
// Function to fetch and display user-generated posts
async function fetchAndDisplayUserGeneratedPosts() {
  try {
      const url = '/user-posts';
      const response = await fetch(url);

      if (!response.ok) {
          throw new Error(`Failed to fetch user-generated posts. Status: ${response.status}`);
      }

      const data = await response.json();

      // Assuming you have a container element with the id "postContainer" to display posts
      const postContainer = document.getElementById('postContainer');

      // Clear existing content in the container
      postContainer.innerHTML = '';

      data.posts.forEach((post) => {
          const postDiv = document.createElement('div');
          postDiv.classList.add('post');

          const titleElement = document.createElement('h2');
          titleElement.textContent = post.title;
          const coverImageDiv = document.createElement('div'); // Container for the cover image
          coverImageDiv.classList.add('cover-image');

          const imageElement = document.createElement('img');
          imageElement.src = `data:image/jpeg;base64,${post.cover_image}`;
          imageElement.alt = post.title;

          const readMoreLink = document.createElement('a');
          readMoreLink.href = `/post_details/${post.id}`;
          readMoreLink.textContent = 'Read More';

          postDiv.appendChild(titleElement);
          postDiv.appendChild(imageElement);
          postDiv.appendChild(readMoreLink);

          postContainer.appendChild(postDiv);
      });
  } catch (error) {
      console.error(`Error Fetching and Displaying user-generated posts: ${error}`);
  }
}

// Event listener for window load
window.addEventListener("load", fetchAndDisplayUserGeneratedPosts);

  // Event listeners for buttons
  const blogButton = document.getElementById('blogButton');
  blogButton.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/createblog';
  });
  
  const postButton = document.getElementById('postButton');
  postButton.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/createpost';
  });