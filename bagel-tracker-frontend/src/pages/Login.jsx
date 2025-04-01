import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { loginUser } from '../services/apiService';
import { login } from '../services/authService';

const LoginSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters'),
});

const Login = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      const response = await loginUser(values);
      login(response.token, response.user);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Failed to login. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container">
      <div className="row justify-content-center mt-5">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h2 className="text-center mb-4">BagelTracker Login</h2>
              
              {error && <div className="alert alert-danger">{error}</div>}
              
              <Formik
                initialValues={{ email: '', password: '' }}
                validationSchema={LoginSchema}
                onSubmit={handleSubmit}
              >
                {({ isSubmitting }) => (
                  <Form>
                    <div className="mb-3">
                      <label htmlFor="email" className="form-label">Email</label>
                      <Field 
                        type="email" 
                        name="email" 
                        className="form-control" 
                        placeholder="Enter your email" 
                      />
                      <ErrorMessage name="email" component="div" className="text-danger" />
                    </div>

                    <div className="mb-3">
                      <label htmlFor="password" className="form-label">Password</label>
                      <Field 
                        type="password" 
                        name="password" 
                        className="form-control" 
                        placeholder="Enter your password" 
                      />
                      <ErrorMessage name="password" component="div" className="text-danger" />
                    </div>

                    <button 
                      type="submit" 
                      className="btn btn-primary w-100" 
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? 'Logging in...' : 'Login'}
                    </button>
                  </Form>
                )}
              </Formik>
              
              <div className="mt-3 text-center">
                <p>Don't have an account? <Link to="/register">Register here</Link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;