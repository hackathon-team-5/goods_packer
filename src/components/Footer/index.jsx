import React from "react";
import "./Footer.css";
import penlIcon from "../../images/pen.svg";
import keyboardIcon from "../../images/keyboard.svg";

const Footer = () => {
  return (
    <section className="footer">
      <button className="footer__button">
        <span>
          <img className="footer__button-img" src={keyboardIcon} alt="" />
        </span>
        Ввести с клавиатуры
      </button>

      <button className="footer__button">
        <span>
          <img className="footer__button-img" src={penlIcon} alt="" />
        </span>
        Изменить состав
      </button>
    </section>
  );
};

export default Footer;
