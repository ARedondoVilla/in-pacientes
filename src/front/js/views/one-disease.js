// MUESTRA TODOS LOS POST DE UNA ENFERMEDAD. AÑADIR BOTON DE SEGUIR ENFERMEDAD.
import React, { useContext, useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { Context } from "../store/appContext";
import { Header } from "../component/header.js";
import { CardFeedCenter } from "../component/card-feed-center.js";
import { NoToken } from "../component/no-token";

export const OneDisease = () => {
	const { store, actions } = useContext(Context);
	const params = useParams();

	useEffect(() => {
		actions.getPostsDisease(params.id);
		actions.getOneDisease(params.id);
	}, []);

	let cardItemsFeedDisease = "";
	if (store.diseasePost.length == 0) {
		cardItemsFeedDisease = (
			<div className="card p-3 text-center">
				<p>Aún no hay ninguna publicacion sobre esta enfermedad</p>
				<div className="row my-3 justify-content-center">
					<Link to="/test">
						<button type="button" className="btn btn-info">
							Crea una publicacion
						</button>
					</Link>
				</div>
			</div>
		);
	} else {
		cardItemsFeedDisease = store.diseasePost.map((post, index) => {
			return (
				<div className="row justify-content-center my-2" key={index}>
					<CardFeedCenter post={post} />
				</div>
			);
		});
	}

	// const cardItemsFeedDisease = store.diseasePost.map((postDisease, index) => {
	// 	return (
	// 		<Link key={index} to={`/post/${postDisease.id}`}>
	// 			<CardFeed post={postDisease} />
	// 		</Link>
	// 	);
	// });

	if (store.token == null) {
		return <NoToken />;
	} else {
		return (
			<div className="container minh-100">
				<div className="row mb-2 justify-content-center">
					<Link to="/test">
						<button type="button" className="btn btn-info">
							Volver a Inicio
						</button>
					</Link>
				</div>
				<div className="row mb-2 justify-content-center">
					<h1>Perfil de enfermedad</h1>
				</div>
				<div className="row mb-2 justify-content-center">
					<Header itemName={store.oneDisease.title} qtyPost={store.diseasePost.length} />
				</div>
				<div className="row justify-content-center">
					<div className="row">
						<h3>Descripción</h3>
					</div>
					<div className="row text-justify">
						<p>{store.oneDisease.description}</p>
					</div>
				</div>
				{/* <div className="row my-4 justify-content-center">
					<Link to="/follow">
						<button type="button" className="btn btn-info">
							Sigue esta enfermedad
						</button>
					</Link>
				</div> */}
				<div className="card-deck d-flex align-content-around flex-wrap">{cardItemsFeedDisease}</div>
			</div>
		);
	}
};
