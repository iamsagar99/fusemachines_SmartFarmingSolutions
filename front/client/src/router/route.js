import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import HomeLayout from "../layout/home.layout";
import homepage from "../pages/homepage";
import CropPage from "../pages/croppredict.page";
import SoilMoisturePredict from "../pages/soilmoisturePredict.page.js";
import PathogenPage from "../pages/pathogen.page.js";
import ErrorPage from "../pages/error.page.js";
import CropHealthPage from "../pages/healthmon.page.js";


const RoutingComponent = () => {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<HomeLayout />}>
                        <Route index element={<CropPage />} />
                        <Route path="soil-moisture-prediction" element={<SoilMoisturePredict/>} />
                        <Route path="pathogen-classifier" element={<PathogenPage/>} />
                        <Route path="crop-health-monitor" element={<CropHealthPage/>} />
                        <Route path="*" element={<ErrorPage/>} />
                    </Route>
                </Routes>
            </BrowserRouter>
        </>
    );
};

export default RoutingComponent;