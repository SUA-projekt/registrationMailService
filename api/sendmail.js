const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).send({ error: 'Method not allowed' });
    return;
  }

  const body = req.body || {};
  const { email, name, surname } = body;

  if (!email) {
    res.status(400).send({ error: 'Missing email' });
    return;
  }

  // Read SMTP credentials from environment
  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT, 10),
    secure: false,
    auth: {
      user: process.env.SMTP_USERNAME,
      pass: process.env.SMTP_PASSWORD
    }
  });

  const mailOptions = {
    from: process.env.MAIL_FROM,
    to: email,
    subject: 'Welcome to Parking Service!',
    text: `Hi ${name || ""} ${surname || ""}, thanks for registering at Parking Service FERI MARIBOR, where no parking spots are free!`
  };

  try {
    await transporter.sendMail(mailOptions);
    res.status(200).send({ message: 'Welcome email sent' });
  } catch (error) {
    res.status(500).send({ error: error.message });
  }
};
