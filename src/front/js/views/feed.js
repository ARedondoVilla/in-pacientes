// PAGINA DONDE INSERTAR TODOS LOS POST DE LAS ENFERMEDADES SEGUIDAS POR EL USUARIO (RESUMEN DE LOS POST)
import React, { useContext, useEffect } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";
import { CardFeed } from "../component/card-feed.js";
import { NoToken } from "../component/no-token";

export const Feed = () => {
	const { store, actions } = useContext(Context);

	useEffect(() => {
		actions.getFeed();
	}, []);

	const cardItemsFeed = store.feed.map((post, index) => {
		return (
			<Link key={index} to={`/post/${post.id}`}>
				<CardFeed post={post} />
			</Link>
		);
	});

	if (store.token == null) {
		return <NoToken />;
	} else {
		return (
			<div className="container">
				<div className="row">
					<h1>Feed de inicio</h1>
				</div>

				<div className="card-deck d-flex justify-content-between">{cardItemsFeed}</div>
			</div>
		);
	}
};
