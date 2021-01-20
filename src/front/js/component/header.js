import React, { useContext, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/header.scss";

export const Header = () => {
	const { store, actions } = useContext(Context);

	useEffect(() => {
		actions.getPostUser();
		actions.getUser();
	}, []);

	return (
		<div className="jumbotron">
			<div className="card mb-3" id="card-header">
				<div className="row no-gutters">
					<div className="col-md-4">
						<img
							src="https://picsum.photos/500/500?random=3"
							className="card-img rounded-circle"
							alt="..."
						/>
					</div>
					<div className="col-md-8">
						<div className="card-body">
							<h5 className="card-title">{store.user.username}</h5>
							<p className="card-text">número de posts</p>
							<p>número de seguidores</p>
							<p className="card-text">
								<small className="text-muted">{store.user.updated_at}</small>
							</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};
