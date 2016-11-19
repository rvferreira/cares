import { combineReducers } from 'redux';
import fuelSavings from './fuelSavingsReducer';
import login from './loginReducer';
import {routerReducer} from 'react-router-redux';

const rootReducer = combineReducers({
  login,
  fuelSavings,
  routing: routerReducer
});

export default rootReducer;
