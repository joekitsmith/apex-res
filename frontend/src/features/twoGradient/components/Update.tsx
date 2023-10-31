import { Button, Stack } from "@mui/material";

type UpdateProps = {
  setUpdateClicked: React.Dispatch<React.SetStateAction<boolean>>;
  setClearClicked: React.Dispatch<React.SetStateAction<boolean>>;
};

export function Update({ setUpdateClicked, setClearClicked }: UpdateProps) {
  const handleUpdateClicked = () => {
    setUpdateClicked(true);
  };
  const handleClearClicked = () => {
    setClearClicked(true);
  };
  return (
    <Stack direction="row" justifyContent="center" spacing={10}>
      <Button
        variant="outlined"
        onClick={handleClearClicked}
        sx={{
          width: "fit-content",
          backgroundColor: "#912727",
          color: "white",
        }}
      >
        Clear
      </Button>
      <Button
        variant="outlined"
        onClick={handleUpdateClicked}
        sx={{
          width: "fit-content",
          backgroundColor: "#30115c",
          color: "white",
        }}
      >
        Update
      </Button>
    </Stack>
  );
}
