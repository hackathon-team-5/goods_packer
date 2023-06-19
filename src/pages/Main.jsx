import React from "react";
import Header from "../components/Header";
import Content from "../components/Content";
import Footer from "../components/Footer"

const Main = (props) => {
  const { data } = props;
  return (
    <>
      <Header />
      <Content data={data} />
      <Footer />
    </>
  );
};

export default Main;
