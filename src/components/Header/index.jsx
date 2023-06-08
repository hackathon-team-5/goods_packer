import React from "react";
import "./Header.css";
import burgerMenuLogo from "../../images/burger.svg";
import yandexLogo from "../../images/yandex.svg";
import yMarketLogo from "../../images/ymarket.svg";
import buttonLogo from "../../images/Button.svg";
import rocketLogo from "../../images/rocket.svg";

const Header = () => {
  return (
    <section className="header">
      <ul className="header-nav__list">
        <li className="header-nav__list-item">
          <img src={burgerMenuLogo} alt="Меню" />
        </li>
        <li className="header-nav__list-item">
          <img src={yandexLogo} alt="Логотип" />
        </li>
        <li className="header-nav__list-item">
          <img src={yMarketLogo} alt="Логотип" />
        </li>
        <li className="header-nav__list-item">
          <h1 className="header-nav__list-title">Склад</h1>
        </li>
      </ul>
      <h2 className="header-nav__list-title_second">Упаковка</h2>
      <div className="header__right-side-container">
        <div className="header__user-menu">
          <p className="header__user-menu-paragraph">sof-natgemokee</p>
          <button className="header__user-menu-button" type="button">
            <span>
              <img
                className="header__user-menu-button-icon"
                src={rocketLogo}
                alt=""
              />
            </span>
            79%
          </button>
        </div>
        <img src={buttonLogo} alt="" />
      </div>
    </section>
  );
};

export default Header;
