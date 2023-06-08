import React from "react";
import ScanningBox from "../components/ScanningBox";
import Header from "../components/Header";
import Footer from "../components/Footer";

const Skanning = (props) => {
  const { typeBox } = props;
  return (
    <>
      <Header />
      <ScanningBox typeBox={typeBox} />
      <Footer />
    </>
  );
};

export default Skanning;
