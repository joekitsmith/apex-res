import { useNavigate } from "react-router-dom";

import { Layout } from "../components/Layout";
import { LoginBox } from "../components/LoginBox";

export const Login = () => {
  const navigate = useNavigate();

  return (
    <Layout title="Log in to your account">
      <LoginBox onSuccess={() => navigate("/")} />
    </Layout>
  );
};
