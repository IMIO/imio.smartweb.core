import React from "react";
import ContentLoader from "react-content-loader";

const Skeleton = (props) => (
    <ContentLoader
        speed={2}
        viewBox="0 0 710.04 150"
        backgroundColor="#f3f3f3"
        foregroundColor="#ecebeb"
        className="skeleton"
        {...props}
    >
        <rect className="cls-1" width="246" height="150" />
        <rect className="cls-1" x="275.74" width="225.04" height="18.87" />
        <rect className="cls-1" x="275.74" y="47.43" width="434.3" height="10.19" />
        <rect className="cls-1" x="275.74" y="78.06" width="434.3" height="10.19" />
    </ContentLoader>
);

export default Skeleton;
