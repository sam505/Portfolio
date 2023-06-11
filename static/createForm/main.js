// Regular expression from W3C HTML5.2 input specification:
// https://www.w3.org/TR/html/sec-forms.html#email-state-typeemail
var emailRegExp = 
/^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;

const Vue = window.vue;

new Vue({
  // root node
  el: "#app",
  // the instance state
  methods: {
    // validate by type and value
    validate: function(type, value) {
      if (type === "email") {
        this.email.valid = this.isEmail(value) ? true : false;
      }
    },
    // check for valid email adress
    isEmail: function(value) {
      return emailRegExp.test(value);
    },
    // check or uncheck all
    checkAll: function(event) {
      this.selection.features = event.target.checked ? this.features : [];
    }
  },
  watch: {
    // watching nested property
    "email.value": function(value) {
      this.validate("email", value);
    }
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const submit = document.querySelector('#submit');

  document.querySelector('#addmore_exp').onclick = () => {
    const li = document.createElement('li');
    li.innerHTML = `{% include 'user_interface/experience.html' %}`;
    document.querySelector('#experiences_added').append(li);
    return false;
  }

  document.querySelector('#addmore_edu').onclick = () => {
    const p = document.createElement('p');
    p.innerHTML = `{% include 'user_interface/education.html' %}`;
    document.querySelector('#educations_added').append(p);
    return false;
  }

  document.querySelector('#addmore_projects').onclick = () => {
    const li = document.createElement('li');
    li.innerHTML = `{% include 'user_interface/project.html' %}`;
    document.querySelector('#projects_added').append(li);
    return false;
  }

  document.querySelector('#addmore_skills').onclick = () => {
    const li = document.createElement('li');
    li.innerHTML = `{% include 'user_interface/skillset.html' %}`;
    document.querySelector('#skillsets_added').append(li);
    return false;
  }

});