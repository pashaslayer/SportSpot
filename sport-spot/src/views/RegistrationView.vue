<template>
  <div class="container">
    <div class="text-center mt-5">
      <!-- First Row (1 Column) -->
      <div class="row text-center mx-auto">
        <div class="col-md-12">
          <!-- draggable verhindert das verschieben von images -->
          <img
            v-if="!wheelAnimation"
            src="@/assets/logo_vektor_01_white.svg"
            class="rounded mx-auto d-block img-fluid"
            draggable="false"
          />
          <img
            v-if="wheelAnimation"
            src="@/assets/logo_vektor_01_white.svg"
            class="rounded mx-auto d-block wheel-animation img-fluid"
            draggable="false"
            @animationend="stopWheelAnimation"
          />
          <h1>{{ title }}</h1>
        </div>
      </div>

      <form @submit.prevent="postRegister">
        <!-- @submit.prevent="postRegister"> -->
        <div class="row">
          <div
            class="col-md-2 border border-white align-items-center d-flex justify-content-center"
          >
            <label for="firstname" class="form-label">Firstname:</label>
          </div>
          <div class="col-md-2 border border-white">
            <input
              v-model="postData.firstname"
              type="text"
              class="form-control"
              id="firstname-label"
            />
          </div>
          <div
            class="col-md-2 border border-white align-items-center d-flex justify-content-center"
          >
            <label for="username" class="form-label">Username: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Benutzername-->
            <input
              v-model="postData.username"
              type="text"
              class="form-control"
              id="username-label"
              minlength="6"
              maxlength="10"
            />
          </div>
          <div
            class="col-md-2 border border-white align-items-center d-flex justify-content-center"
          >
            <label for="email-label" class="form-label">Email: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Email-->
            <input
              v-model="postData.email"
              type="email"
              id="email-label"
              class="form-control"
              aria-describedby="emailHelp"
              required
            />
          </div>
        </div>

        <!-- Third Row (6 Columns) -->
        <div class="row">
          <div
            class="col-md-2 border border-white align-items-center d-flex justify-content-center"
          >
            <label for="surname" class="form-label">Surname: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Nachname-->
            <input
              v-model="postData.surname"
              type="text"
              class="form-control"
              id="surname-label"
            />
          </div>
          <div
            class="col-md-2 border border-white align-items-center d-flex justify-content-center"
          >
            <label for="password" class="form-label">Password: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Passwort-->
            <input
              v-model="postData.password"
              type="password"
              class="form-control"
              id="password-label"
              aria-describedby="passwordHelp"
              required
            />
          </div>
          <div
            class="col-md-2 border border-white align-items-center d-flex justify-content-center"
          >
            <label for="postalcode" class="form-label">Postalcode: </label>
          </div>
          <div class="col-md-2 border border-white">
            <!--Input Plz-->
            <input
              v-model="postData.postalcode"
              type="text"
              class="form-control"
              id="postalcode-label"
              maxlength="8"
            />
          </div>
        </div>

        <!-- Fourth Row (Spacing) -->
        <div class="row" style="height: 20px"></div>

        <div class="row" style="height: 30px">
          <div class="col-md-6">Date</div>
          <div class="col-md-6">Gender</div>
        </div>

        <!-- Fifth Row (2 Columns) -->
        <div class="row">
          <div class="col-md-6">
            <input
              id="startDate"
              class="form-control"
              type="date"
              v-model="postData.birthdate"
            />
          </div>
          <div class="col-md-6">
            <select
              v-model="postData.gender"
              id="sports"
              class="form-select"
              required
            >
              <option value="male">male</option>
              <option value="female">female</option>
              <option value="other">other</option>
            </select>
          </div>
        </div>

        <div class="row" style="height: 80px"></div>

        <div class="d-flex justify-content-center">
          <span class="mr-2">Bereits registriert?: </span>
          <router-link to="/login">Login</router-link>
        </div>

        <!-- Sixth Row (2 Columns for Buttons) -->
        <div class="row">
          <div class="col-md-6 d-flex justify-content-end">
            <button class="btn btn-primary">
              Bestätigen
            </button>
          </div>
          <div class="col-md-6 d-flex justify-content-start">
            <button class="btn btn-secondary" @click="clear">Abbrechen</button>
          </div>
        </div>
      </form>
    </div>

    <div v-if="testing" class="info">
      <p>Firstname: {{ postData.firstname }}</p>
      <p>Surname: {{ postData.surname }}</p>
      <p>Username: {{ postData.username }}</p>
      <p>Password: {{ postData.password }}</p>
      <p>Birthdate: {{ postData.birthdate }}</p>
      <p>Email: {{ postData.email }}</p>
      <p>Sports: {{ postData.sports }}</p>
      <p>Gender: {{ postData.gender }}</p>
      <p>Postalcode: {{ postData.postalcode }}</p>
    </div>
  </div>
</template>

<!--
Daten für die Userregistrierung
•    Vorname
•    Nachname
•    Benutzername
•    Passwort
•    Geburtstag
•    Email
•    Bevorzugte Sportarten
•    Geschlecht
•    Postleizahl
-->

<style>
.border-bottom-remove {
  border-bottom: none !important;
}

.info {
  border: 2px;
  border-color: black;
  border-style: solid;
  margin-left: 6vw;
  margin-right: 6vw;
  margin-bottom: 1cm;
}

img {
  /* Verhindert das Auswählen vom image */
  user-select: none;
}

/* Logik für das Drehen vom Logo */
@keyframes wheelSpin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>

<script>
import axios from "axios";

export default {
  data() {
    return {
      title: "SportSpot Registrierung",
      // Kleines Fenster zur Anzeige von Userinputs bei Verstellung des (testing) Wertes wird dieses angezeigt oder versteckt
      testing: false,
      wheelAnimation: false,
      postData: {
        firstname: "",
        surname: "",
        username: "",
        password: "",
        birthdate: "",
        email: "",
        sports: [],
        gender: "",
        postalcode: "",
      },
    };
  },
  methods: {
    postRegister() {
      axios
        .post("http://127.0.0.1:5000/register", this.postData)
        .then((response) => {
          console.log(response);
          this.startWheelAnimation();

          // Holen von vue email
          const email = this.postData.email;


          setTimeout(() => {
            this.$router.push({ path: '/pickSports', query: { email } });
          }, 2000);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    clear() {
      // löscht alle bisher eingetragenen inputs
      this.postData.firstname = "";
      this.postData.surname = "";
      this.postData.username = "";
      this.postData.password = "";
      this.postData.birthdate = "";
      this.postData.email = "";
      this.postData.sports = [];
      this.postData.gender = "";
      this.postData.firstname = "";
      this.postData.postalcode = "";
    },
    startWheelAnimation() {
      this.wheelAnimation = true;
    },
    stopWheelAnimation() {
      this.wheelAnimation = false;
    },
  },
};

// JWT Token

// localStorage.setItem("Name", "Bob");
// localStorage.getItem('Name');
// localStorage.removeItem('Name');
</script>
