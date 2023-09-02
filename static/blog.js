document.addEventListener('DOMContentLoaded', () => {
    const blogCreation = document.querySelector('.blogcreation');
  
    blogCreation.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const name = document.getElementById('name').value;
      const category = document.getElementById('category').value;
      console.log('Form submitted with data:',name,category);
      try {
        const response = await fetch('http://127.0.0.1:5000/blog', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: name,
            category:category
          })
        });
        
        if (response.ok) {
          const data = await response.json();
          alert(data.message);
          window.location.href='http://127.0.0.1:5000/home';
        } else {
          const errorData = await response.json();
          window.location.href='http://127.0.0.1:5000/createblog';
          alert("error: " + errorData.error);
        }
        } catch(error){
          console.log('An error occurred',error);
          window.location.href='http://127.0.0.1:5000/createblog';
        }
    });
  });