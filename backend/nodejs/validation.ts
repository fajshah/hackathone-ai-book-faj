import Joi from 'joi';
import { Request, Response, NextFunction } from 'express';

// Validation schemas
const schemas = {
  askQuery: Joi.object({
    query: Joi.string().min(1).max(1000).required(),
  }),

  userLogin: Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().min(6).max(100).required(),
  }),

  userRegister: Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().min(6).max(100).required(),
    firstName: Joi.string().min(1).max(50).required(),
    lastName: Joi.string().min(1).max(50).required(),
  }),

  conversation: Joi.object({
    query: Joi.string().min(1).max(1000).required(),
    answer: Joi.string().min(1).max(10000).required(),
  }),
};

// Validation middleware factory
export const validate = (schema: keyof typeof schemas) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const { error } = schemas[schema].validate(req.body, {
      abortEarly: false, // Return all validation errors
      stripUnknown: true // Remove unknown properties
    });

    if (error) {
      const errors = error.details.map(detail => detail.message);
      return res.status(400).json({
        error: 'Validation error',
        details: errors,
      });
    }

    next();
  };
};

// Query validation middleware for GET requests
export const validateQuery = (schema: Joi.ObjectSchema) => {
  return (req: Request, res: Response, next: NextFunction) => {
    const { error } = schema.validate(req.query, {
      abortEarly: false,
      stripUnknown: true
    });

    if (error) {
      const errors = error.details.map(detail => detail.message);
      return res.status(400).json({
        error: 'Query validation error',
        details: errors,
      });
    }

    next();
  };
};