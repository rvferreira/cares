import delay from './delay';

const users = [
  {
    email: 'raph@gd.com',
    firstName: 'Raphael',
    lastName: 'Ferreira',
    password: '1234'
  },
  {
    email: 'valeska@gm.com',
    firstName: 'Valeska',
    lastName: 'Paroni',
    password: '1234'
  }
];

class UserApi {
  static create(user) {
    user = Object.assign({}, user); // to avoid manipulating object passed in.
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        // Simulate server-side validation
        const minNameLength = 3;
        if (user.name.length < minNameLength) {
          reject(`Name must be at least ${minNameLength} characters.`);
        }

        if (!user.email.length) {
          reject(`The email field is required.`);
        }

        const existingUserIndex = users.findIndex(u => u.email == user.email);
        if (existingUserIndex) reject(`Email is already being used.`);

        resolve(user);
      }, delay);
    });
  }

  static login(email, password) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {

        const indexOfUser = users.findIndex(u => {
          u.email == email;
          u.password == password;
        });

        console.log(indexOfUser);
        reject();

        console.log(users.splice(indexOfUser, 1));
        resolve();

      }, delay);
    });
  }
}

export default UserApi;
