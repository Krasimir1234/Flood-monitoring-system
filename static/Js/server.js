const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const app = express();
app.use(express.json());


const userSchema = new mongoose.Schema({
  realName: String,
  lastName: String,
  username: { type: String, unique: true }, // Ensure unique usernames
  email: { type: String, unique: true },
  password: String,
  bio: String,
  profileImage: String,
  description: String,
});

const User = mongoose.model('User', userSchema);


app.post('/api/signup', async (req, res) => {
  const { realName, lastName, username, email, password, bio } = req.body;

  try {
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({
      realName,
      lastName,
      username,
      email,
      password: hashedPassword,
      bio,
      profileImage: '',
      description: '',
    });

    await user.save();
    res.json({ userId: user._id });
  } catch (error) {
    res.status(500).json({ message: 'Error saving user' });
  }
});


app.post('/api/login', async (req, res) => {
  const { emailOrUsername, password } = req.body;

  try {
    const query = emailOrUsername.includes('@') ? { email: emailOrUsername } : { username: emailOrUsername };
    const user = await User.findOne(query);

    if (user && await bcrypt.compare(password, user.password)) {
      res.json({ userId: user._id });
    } else {
      res.status(401).json({ message: 'Invalid email/username or password' });
    }
  } catch (error) {
    res.status(500).json({ message: 'Error logging in' });
  }
});

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
