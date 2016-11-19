import * as types from '../constants/actionTypes';
import * as errors from '../constants/errorTypes';

import UserApi from '../api/mockAccountApi';

export function login(email, password) {
  console.log();
  return function (dispatch) {
    UserApi.login(email, password).then(r => {
        console.log(r);
        return dispatch({
          type: types.ACCOUNT_LOGIN,
          data: r
        });
      }
    ).catch(e => {
        console.log(e);
        return dispatch(errors.INVALID_CREDENTIALS);
    });
  };
}
