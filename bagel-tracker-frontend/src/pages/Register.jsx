import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { registerUser } from '../services/apiService';
import { login } from '../services/authService';

const RegisterSchema = Yup.object().shape({
  name: Yup.string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters'),
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), null], 'Passwords must match')
    .required('Confirm password is required'),
});

const Register = () => {
  const navigate = useNavigate();
  const [error, setError] = useState('');

  const handleSubmit = async (values, { setSubmitting }) => {
    try {
      // Remove confirmPassword before sending to API
      const { confirmPassword, ...userData } = values;
      const response = await registerUser(userData);
      login(response.token, response.user);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message || 'Failed to register. Please try again.');
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
              <h2 className="text-center mb-4">BagelTracker Registration</h2>
              
              {error && <div className="alert alert-danger">{error}</div>}
              
              <Formik
                initialValues={{ name: '', email: '', password: '', confirmPassword: '' }}
                validationSchema={RegisterSchema}
                onSubmit={handleSubmit}
              >
                {({ isSubmitting }) => (
                  <Form>
                    <div className="mb-3">
                      <label htmlFor="name" className="form-label">Name</label>
                      <Field 
                        type="text" 
                        name="name" 
                        className="form-control" 
                        placeholder="Enter your name" 
                      />
                      <ErrorMessage name="name" component="div" className="text-danger" />
                    </div>

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

                    <div className="mb-3">
                      <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                      <Field 
                        type="password" 
                        name="confirmPassword" 
                        className="form-control" 
                        placeholder="Confirm your password" 
                      />
                      <ErrorMessage name="confirmPassword" component="div" className="text-danger" />
                    </div>

                    <button 
                      type="submit" 
                      className="btn btn-primary w-100" 
                      disabled={isSubmitting}
                    >
                      {isSubmitting ? 'Registering...' : 'Register'}
                    </button>
                  </Form>
                )}
              </Formik>
              
              <div className="mt-3 text-center">
                <p>Already have an account? <Link to="/login">Login here</Link></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;