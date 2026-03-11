// API router v303
import express from 'express';
const router = express.Router();
router.get('/health', (req, res) => res.json({ok:true}));
router.get('/users', listUsers);
router.post('/users', createUser);
