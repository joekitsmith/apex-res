import React from "react";
import { useD3 } from "../hooks/useD3";
import * as d3 from "d3";
// import "../../../css/style.css";
import { usePredict } from "../api/predict";

export function Chromatogram() {
  const results = usePredict().data;

  const ref = useD3(
    (svg: any) => {
      svg.selectAll("*").remove();

      var parent = svg.node().parentElement;
      var svgWidth = parent.clientWidth;
      var svgHeight = parent.clientHeight;

      const root = svg.append("g");
      root.attr("transform", undefined);

      const margin = { top: 50, right: 70, bottom: 50, left: 70 };

      const xAxisGroup = root
        .append("g")
        .attr(
          "transform",
          `translate(${margin.left}, ${svgHeight - margin.bottom})`
        );

      const yAxisGroup = root
        .append("g")
        .attr(
          "transform",
          `translate(${margin.left}, ${svgHeight - margin.bottom})`
        );

      const xScale = d3
        .scaleLinear()
        .domain([0, 100])
        .range([0, svgWidth - margin.left - margin.right]);

      const yScale = d3
        .scaleLinear()
        .domain([0, 100])
        .range([0, -(svgHeight - margin.top - margin.bottom)]);

      const xAxis = d3.axisBottom(xScale);
      const yAxis = d3.axisLeft(yScale);

      xAxisGroup.call(xAxis);
      yAxisGroup.call(yAxis);
    },
    [results]
  );

  return <svg ref={ref} height="100%" width="100%" />;
}
