import React, {PropTypes} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import * as actions from '../../actions/accountActions';

export const LoginPage = (props) => {
  return (
    <div>
      <span>User: {JSON.stringify(props.login)}</span>
      <button onClick={props.actions.login("raph@gd.com", "1234")} />
    </div>
  );
};

LoginPage.propTypes = {
  actions: PropTypes.object.isRequired,
  login: PropTypes.object.isRequired,
};

function mapStateToProps(state) {
  return {
    login: state.login
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch)
  };
}

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(LoginPage);
