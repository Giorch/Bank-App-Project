import axios from "axios"
const API_URL = "https://bank-app-project-cpxu.onrender.com/api"

export const getAllCustomers = () =>
    axios.get(`${API_URL}/customers`);

export const getCustomerById = (id) =>
    axios.get(`${API_URL}/customers/${id}`);

export const getCustomerByName = (name) =>
    axios.get(`${API_URL}/customers/search?name=${name}`);

export const getPremiumCustomers = () =>
    axios.get(`${API_URL}/customers/premium`);

export const createCustomer = (customer) =>
    axios.post(`${API_URL}/customers`, customer);

export const updateCustomer = (id, customer) =>
    axios.put(`${API_URL}/customers/${id}`, customer);

export const deleteCustomer = (id) =>
    axios.delete(`${API_URL}/customers/${id}`);

export const getAllAccounts = () =>
    axios.get(`${API_URL}/accounts`);

export const getAccountById = (id) =>
    axios.get(`${API_URL}/accounts/${id}`);

export const createAccount = (customerId, account) =>
    axios.post(`${API_URL}/accounts?customerId=${customerId}`, account);

export const updateAccount = (id, account) =>
    axios.put(`${API_URL}/accounts/${id}`, account);

export const deleteAccount = (id) =>
    axios.delete(`${API_URL}/accounts/${id}`);