import {ACCOUNT_LOGIN} from '../constants/actionTypes';
import {INVALID_CREDENTIALS} from '../constants/errorTypes';
import objectAssign from 'object-assign';

export default function (state = {}, action) {

  switch (action.type) {
    case ACCOUNT_LOGIN:
      return objectAssign({}, action.data);
    case INVALID_CREDENTIALS:
      return objectAssign({}, action.data);
    default:
      return state;
  }
}
