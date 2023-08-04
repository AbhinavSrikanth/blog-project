document.addEventListener('DOMContentLoaded', () => {
    const blogCreation = document.querySelector('.blogcreation');
  
    blogCreation.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const name = document.getElementById('name').value;
      const email = document.getElementById('email').value;
      const category = document.getElementById('category').value;
      console.log('Form submitted with data:',name,email,category);

      try {
        const response = await fetch('http://127.0.0.1:5000/blog', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: name,
            email: email,
            category:category
          })
        });
        console.log('Response status:',response.status);
        if (response.ok) {
          const data = await response.json();
          alert(data.message);
          console.log('Success:',data.message);
        } else {
          const errorData = await response.json();
          alert(errorData.error);
          console.log('Error:',errorData.error);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.');
      }
    });

    function redirectToHome(){
      console.log("dfghj")
      window.location.href='../home/home.html';
    }
  });
   