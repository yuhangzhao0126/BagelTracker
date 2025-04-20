import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { registerUser } from '../services/apiService';
import { login } from '../services/authService';

const RegisterSchema = Yup.object().shape({
  name: Yup.string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters')
    .matches(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),
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
  const [fieldErrors, setFieldErrors] = useState({});

  const handleSubmit = async (values, { setSubmitting, setFieldError }) => {
    try {
      // Clear previous errors
      setError('');
      setFieldErrors({});
      
      // Remove confirmPassword before sending to API
      const { confirmPassword, ...userData } = values;
      const response = await registerUser(userData);
      
      if (response.success) {
        login(response.token, response.user);
        navigate('/dashboard');
      } else {
        // Handle specific error messages from the backend
        if (response.message.includes('Email already registered')) {
          setFieldError('email', 'This email is already registered');
          setFieldErrors(prev => ({ ...prev, email: 'This email is already registered' }));
        } else if (response.message.includes('Username already taken')) {
          setFieldError('name', 'This username is already taken');
          setFieldErrors(prev => ({ ...prev, name: 'This username is already taken' }));
        } else {
          setError(response.message || 'Failed to register. Please try again.');
        }
      }
    } catch (err) {
      // Handle general errors
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
                {({ isSubmitting, errors }) => (
                  <Form>
                    <div className="mb-3">
                      <label htmlFor="name" className="form-label">Username</label>
                      <Field 
                        type="text" 
                        name="name" 
                        className={`form-control ${errors.name || fieldErrors.name ? 'is-invalid' : ''}`}
                        placeholder="Choose a unique username" 
                      />
                      <small className="form-text text-muted">Username must be unique and can only contain letters, numbers, and underscores.</small>
                      <ErrorMessage name="name" component="div" className="text-danger" />
                      {fieldErrors.name && <div className="text-danger">{fieldErrors.name}</div>}
                    </div>

                    <div className="mb-3">
                      <label htmlFor="email" className="form-label">Email</label>
                      <Field 
                        type="email" 
                        name="email" 
                        className={`form-control ${errors.email || fieldErrors.email ? 'is-invalid' : ''}`}
                        placeholder="Enter your email" 
                      />
                      <ErrorMessage name="email" component="div" className="text-danger" />
                      {fieldErrors.email && <div className="text-danger">{fieldErrors.email}</div>}
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