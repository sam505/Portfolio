window.onload = function () {
  // Get the body element
  var body = document.body;

  // Get the button element
  var button = document.getElementById("lightSwitch");

  // Add event listener to the button
  button.addEventListener("change", function () {
    // Toggle the class on the body
    body.classList.toggle("drak");
  });
};
