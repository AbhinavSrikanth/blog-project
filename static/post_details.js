document.addEventListener('DOMContentLoaded', async () => {
  function extractPostIdFromUrl() {
    const currentUrl = window.location.href;
    const parts = currentUrl.split('/');
    return parts[parts.length - 1];
  }

  const postId = extractPostIdFromUrl();
  const commentForm = document.querySelector('#comment-form');
  const commentsList = document.querySelector('#comments-list'); // Assuming you have an element with id="comments-list"

  function appendCommentItem(authorName, commentText) {
    const commentItem = document.createElement('li');
    commentItem.innerHTML = `<strong>${authorName}:</strong> ${commentText}`;
    commentsList.appendChild(commentItem);
  }

  async function fetchAndDisplayComments() {
    try {
      const response = await fetch(`http://127.0.0.1:5000/comments/${postId}`);

      if (response.ok) {
        const existingComments = await response.json();
        commentsList.innerHTML = '';
        existingComments.forEach((comment) => {
          appendCommentItem(comment.author_name, comment.comment);
        });
      } else {
        console.log('Error:', response.status);
      }
    } catch (error) {
      console.log('An error occurred while fetching existing comments', error);
    }
  }

  fetchAndDisplayComments();

  commentForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const comment = document.getElementById('comment').value;
    const formData = new FormData();
    formData.append('comment', comment);
    formData.append('post_id', postId);

    try {
      const response = await fetch('http://127.0.0.1:5000/comments', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        console.log('Comment submitted successfully');

        document.getElementById('comment').value = '';

        fetchAndDisplayComments();
      } else {
        console.log('Error:', response.status);
      }
    } catch (error) {
      console.log('An error occurred', error);
    }
  });
});