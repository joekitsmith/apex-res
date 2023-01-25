import { useNavigate } from "react-router-dom";

import { Layout } from "../components/Layout";
import { RegisterBox } from "../components/RegisterBox";

export const Register = () => {
  const navigate = useNavigate();

  return (
    <Layout title="Log in to your account">
      <RegisterBox onSuccess={() => navigate("/app")} />
    </Layout>
  );
};
