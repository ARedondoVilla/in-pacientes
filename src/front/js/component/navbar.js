import React, { useContext, useEffect } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";
// import Logo from "../../img/logo.jpg";
// import Smlogo from "../../img/smlogo.jpg";
import logonavbar from "../../img/logonavbar.jpg";
import "../../styles/navbar.scss";

export const Navbar = () => {
	const { store, actions } = useContext(Context);

	useEffect(
		() => {
			actions.getUser();
		},
		[store.token]
	);

	if (store.token == null) {
		return (
			<nav className="navbar bg-light">
				<div className="p-2 flex-grow-1 bd-highlight">
					<Link to="/">
						<img id="smlogo" src={logonavbar} />
					</Link>
				</div>
				<div className="p-2 bd-highlight">
					<Link to="/diseases">
						<span>Enfermedades</span>
					</Link>
				</div>
				<div className="p-2 bd-highlight">
					<Link to="/associations">
						<span>Asociaciones</span>
					</Link>
				</div>
				<div className="p-2 bd-highlight">
					<Link to="/about-us">
						<span>About Us</span>
					</Link>
				</div>
			</nav>
		);
	} else {
		return (
			<nav className="navbar bg-light">
				<div className="p-2 flex-grow-1 bd-highlight">
					<Link to="/">
						<img id="smlogo" src={logonavbar} />
					</Link>
				</div>

				<div className="p-2 bd-highlight">
					<Link to="/inicio">
						<span>Inicio</span>
					</Link>
				</div>
				{/* <div className="p-2 bd-highlight">
					<Link to="/feed">
						<span>Publicaciones</span>
					</Link>
				</div> */}
				<div className="p-2 bd-highlight">
					<Link to="/diseases">
						<span>Enfermedades</span>
					</Link>
				</div>
				<div className="p-2 bd-highlight">
					<Link to="/associations">
						<span>Asociaciones</span>
					</Link>
				</div>
				<div className="p-2 bd-highlight">
					<Link to="/about-us">
						<span>About Us</span>
					</Link>
				</div>
				<div className="">
					<Link to="/profile" className="p-2 bd-highlight color-username">
						<span>{store.user.username}</span>
					</Link>
				</div>
				<div className="p-2 bd-highlight">
					<Link to="/bye" type="button" onClick={() => actions.logout()} style={{ color: "grey" }}>
						Cerrar sesión
					</Link>
				</div>
			</nav>
		);
	}
};
