import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";

const firebaseConfig = {
  apiKey: "MOCK_API_KEY",
  authDomain: "mock-agri-nexus.firebaseapp.com",
  databaseURL: "https://mock-agri-nexus-default-rtdb.firebaseio.com",
  projectId: "mock-agri-nexus",
  storageBucket: "mock-agri-nexus.appspot.com",
  messagingSenderId: "1234567890",
  appId: "1:1234567890:web:abcdef"
};

const app = initializeApp(firebaseConfig);
export const database = getDatabase(app);
