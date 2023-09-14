document.addEventListener('DOMContentLoaded', () => {
    const postForm = document.querySelector('.postcreation');
  
    postForm.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const title = document.getElementById('title').value;
      const content = document.getElementById('content').value;
      const blogname=document.getElementById('blogname').value;
      const fileInput=document.getElementById('coverImage').files[0];
      
      const formData = new FormData();
      formData.append('title', title);
      formData.append('content', content);
      formData.append('blogname',blogname);
      formData.append('coverImage',fileInput);
      try {
        const response = await fetch('http://127.0.0.1:5000/post', {
          method: 'POST',

          body: formData
        });
        
        if (response.ok) {
          const blob = await response.blob();
          const downloadLink = document.createElement('a');
          downloadLink.href = window.URL.createObjectURL(blob);
          downloadLink.download = 'filename.jpg';
          downloadLink.style.display = 'none';
          document.body.appendChild(downloadLink);
          downloadLink.click();
          document.body.removeChild(downloadLink);
          window.location.href='http://127.0.0.1:5000/home';
        } else {
          const errorData = await response.json();
          alert("Error: " + errorData.error);
          if(errorData.error==="Blogname does not exist") {
          document.getElementById('blogname').value='';
          window.location.href='http://127.0.0.1:5000/createpost';
        }
      }
        } catch(error){
            console.log('Error Details',error)
            alert('An error occurred. Please try again later.');
            window.location.href='http://127.0.0.1:5000/createpost';
        }
    });
  });
  