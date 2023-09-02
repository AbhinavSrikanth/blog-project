const blogButton=document.getElementById('blogButton');
blogButton.addEventListener('click', () => {
  window.location.href = 'http://127.0.0.1:5000/createblog';
});
const postButton=document.getElementById('postButton');
postButton.addEventListener('click', () => {
  window.location.href = 'http://127.0.0.1:5000/createpost';
});