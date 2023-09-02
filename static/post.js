document.addEventListener('DOMContentLoaded', () => {
    const postForm = document.querySelector('.postcreation');
  
    postForm.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const title = document.getElementById('title').value;
      const content = document.getElementById('content').value;
      const fileInput = document.getElementById('file').files[0];
  
      const formData = new FormData();
      formData.append('title', title);
      formData.append('content', content);
      try {
        const response = await fetch('http://127.0.0.1:5000/post', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: title,
            content: content,
            fileInput:fileInput,
            blogname:blogname
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          alert(data.message);
          window.location.href='http://127.0.0.1:5000/home';
        } else {
          const errorData = await response.json();
          alert("error: " + errorData.error);
        }
        } catch(error){
            console.log('Error Details',error)
            alert('An error occurred. Please try again later.');
        }
    });
  });
  