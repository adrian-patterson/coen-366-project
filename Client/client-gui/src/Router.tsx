import { FC } from "react";
import { Route, Routes } from "react-router-dom";
import App from "./App";
import WelcomePage from "./WelcomePage";

export type IRouter = {};

export const Router: FC<IRouter> = () => {
  return (
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/app" element={<App />} />
    </Routes>
  );
};

export default Router;
