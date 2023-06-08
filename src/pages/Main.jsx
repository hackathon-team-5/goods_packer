import React from "react";
import Header from "../components/Header";
import Content from "../components/Content";

const Main = (props) => {
  const { data } = props;
  return (
    <>
      <Header />
      <Content data={data} />
    </>
  );
};

export default Main;
