document.addEventListener('DOMContentLoaded', () => {
    const postForm = document.querySelector('.postcreation');
  
    postForm.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const title = document.getElementById('title').value;
      const content = document.getElementById('content').value;
      const fileInput = document.getElementById('file').files[0];
  
      const formData = new FormData();
      formData.append('post_title', title);
      formData.append('content', content);
      //formData.append('file', fileInput);
      try {
        const response = await fetch('http://127.0.0.1:5000/blogfrontend/post', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: title,
            content: content,
            file:file
          })
        });
        
        console.log('Response status:', response.status);
        if (response.ok) {
          const data = await response.json();
          alert(data.message);
          console.log('Success:', data.message);
        } else {
          const errorData = await response.json();
          alert(errorData.error);
          console.log('Error:', errorData.error);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
      }
    });
  });
  